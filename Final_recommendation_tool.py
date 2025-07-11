from datetime import datetime, timedelta
from final_synthetic_routing import (
    get_roundtrip, one_way, get_oneway_options,
    valid_layover, Origin, Destination, Departure_Date, Return_Date, Hubs, Airline_Whitelist, min_layover, Headers
)
from value_per_mile import get_value_per_mile_airlines, value_per_mile_giftCards, value_per_mile_hotels

def create_route_object(route_type, carrier, price, miles, class_code="Y", synthetic=False, legs=None, roundTrip = False):
    if route_type == "flight":
        if synthetic:
            vpms = []
            for leg in legs:
                vpms.append(get_value_per_mile_airlines(leg["airline"], class_code))
            vpm = sum(vpms) / len(vpms)
        else:
            vpm = get_value_per_mile_airlines(carrier, class_code)
    elif route_type == "gift_card":
        vpm = value_per_mile_giftCards(carrier)
    elif route_type == "hotel":
        vpm = value_per_mile_hotels(carrier)

    return {
        "type": route_type,
        "airline": carrier,
        "price": round(price, 2),
        "total_distance": miles,
        "vpm": round(vpm, 2) if vpm else 0,
        "synthetic": synthetic,
        "roundtrip": roundTrip,
        "legs": legs
    }

def recommend_routes(routes, priority):
    if priority not in {"distance", "value_per_mile", "price"}:
        raise ValueError("Priority must be one of: 'distance', 'value_per_mile', 'price'")
    if priority == "distance":
        key = lambda r: r["total_distance"]
        reverse = False
    elif priority == "value_per_mile":
        key = lambda r: r["vpm"]
        reverse = True
    elif priority == "price":
        key = lambda r: r["price"]
        reverse = False
    return sorted(routes, key=key, reverse=reverse)[:5]

def gather_all_routes():
    flight_routes_out = []
    flight_routes_in = []
    
    roundtrip_data = get_roundtrip(Origin, Destination, Departure_Date, Return_Date)
    if roundtrip_data:
        slices = roundtrip_data["slice_data"]
        out = slices.get("slice_0")
        inn = slices.get("slice_1")
        out_price = round(float(roundtrip_data["price_details"]["display_total_fare"]) / 2, 2)
        out_airline = out["airline"]["code"]
        out_dep = datetime.fromisoformat(out["departure"]["datetime"]["date_time"])
        out_arr = datetime.fromisoformat(out["arrival"]["datetime"]["date_time"])
        flight_routes_out.append(create_route_object(
                "flight", out["airline"]["code"], float(roundtrip_data["price_details"]["display_total_fare"]), 2200,
                legs=[{
                    "airline": out_airline,
                    "price": out_price,
                    "departure": out_dep,
                    "arrival": out_arr,
                    "origin": out["departure"]["airport"]["code"],
                    "destination": out["arrival"]["airport"]["code"]
                }],
                roundTrip=True
            ))

        in_price = round(float(roundtrip_data["price_details"]["display_total_fare"]) / 2, 2)
        in_airline = inn["airline"]["code"]
        in_dep = datetime.fromisoformat(inn["departure"]["datetime"]["date_time"])
        in_arr = datetime.fromisoformat(inn["arrival"]["datetime"]["date_time"])
        flight_routes_in.append(create_route_object(
                "flight", inn["airline"]["code"], float(roundtrip_data["price_details"]["display_total_fare"]), 2200,
                legs=[{
                    "airline": in_airline,
                    "price": in_price,
                    "departure": in_dep,
                    "arrival": in_arr,
                    "origin": inn["departure"]["airport"]["code"],
                    "destination": inn["arrival"]["airport"]["code"]
                }],
                roundTrip=True
            ))

    valid_out = []
    valid_in = []
    for hub in Hubs:
        if hub in [Origin, Destination]:
            continue
        leg1_options = get_oneway_options(Origin, hub, Departure_Date)
        leg2_options = get_oneway_options(hub, Destination, Departure_Date)
        out = valid_layover(leg1_options, leg2_options, hub)
        if out:
            valid_out.append(out)
        leg3_options = get_oneway_options(Destination, hub, Return_Date)
        leg4_options = get_oneway_options(hub, Origin, Return_Date)
        inn = valid_layover(leg3_options, leg4_options, hub)
        if inn:
            valid_in.append(inn)

    if valid_out:
        # Add multiple outbound synthetic routes (up to 3 best options)
        sorted_valid_out = sorted(valid_out, key=lambda x: x["price"])[:3]
        for best_out in sorted_valid_out:
            total_price = best_out["price"]
            legs = [
                {**best_out["leg1"], "origin": Origin, "destination": best_out["hub"]},
                {**best_out["leg2"], "origin": best_out["hub"], "destination": Destination}
            ]
            flight_routes_out.append(
                create_route_object("flight", "MULTI", total_price, 1100, synthetic=True, legs=legs)
            )
    if valid_in:
        # Add multiple inbound synthetic routes (up to 3 best options)
        sorted_valid_in = sorted(valid_in, key=lambda x: x["price"])[:3]
        for best_in in sorted_valid_in:
            total_price = best_in["price"]
            legs = [
                {**best_in["leg1"], "origin": Destination, "destination": best_in["hub"]},
                {**best_in["leg2"], "origin": best_in["hub"], "destination": Origin}
            ]
            flight_routes_in.append(
                create_route_object("flight", "MULTI", total_price, 1100, synthetic=True, legs=legs)
            )

    gift_card_routes = [
        create_route_object("gift_card", "DL", 100, 300),
        create_route_object("gift_card", "UA", 120, 300)
    ]

    hotel_routes = [
        create_route_object("hotel", "AA", 90, 300),
        create_route_object("hotel", "DL", 160, 400)
    ]

    return flight_routes_out,flight_routes_in, gift_card_routes + hotel_routes

def display_recommendations(routes, priority, direction):
    print(f"\nTop {len(routes)} {direction} redemption options by '{priority}':\n")
    for i, route in enumerate(routes, 1):
        label = "SYN" if route.get("synthetic") else ("RT" if route.get("roundtrip") else "DIR")
        print(f"{i}. {label} {route['type'].upper()} | {route['airline']} | "
              f"Price: ${route['price']} | Distance: {route['total_distance']} mi | "
              f"VPM: {route['vpm']}¢/mile")
        if route.get("legs"):
            for j, leg in enumerate(route["legs"], 1):
                dep = leg["departure"] if isinstance(leg["departure"], str) else leg["departure"].strftime("%a %b %d, %I:%M %p")
                arr = leg["arrival"] if isinstance(leg["arrival"], str) else leg["arrival"].strftime("%a %b %d, %I:%M %p")
                print(f"   Leg {j}: {leg['airline']} | ${leg['price']} | {leg['origin']} → {leg['destination']} | {dep} → {arr}")

def display_misc_routes(routes, priority):
    print(f"\nOther redemption options by {priority}:\n")
    sorted_routes = recommend_routes(routes, priority)
    for i, route in enumerate(sorted_routes, 1):
        print(f"{i}. {route['type'].upper()} | {route['airline']} | "
              f"Price: ${route['price']} | Distance: {route['total_distance']} mi | "
              f"VPM: {route['vpm']}¢/mile")


# Run example only if this module is run directly
if __name__ == "__main__":
    try:
        priority = "value_per_mile"
        all_routes_out, all_routes_in, misc_routes = gather_all_routes()
        top_out = recommend_routes(all_routes_out, priority)
        top_in = recommend_routes(all_routes_in, priority)
        display_recommendations(top_out, priority, direction="outbound")
        display_recommendations(top_in, priority, direction="inbound")
        display_misc_routes(misc_routes, priority)
    except Exception as e:
        print(f"Error running example: {e}")
