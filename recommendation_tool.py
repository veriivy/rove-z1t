from Synthetic_Routing import (
    get_roundtrip, one_way, get_oneway_options,
    valid_layover, Origin, Destination, Departure_Date, Return_Date, Hubs, Airline_Whitelist, min_layover, Headers
)
from VPM import get_value_per_mile_airlines, value_per_mile_giftCards, value_per_mile_hotels
# Typical Python naming conventions:
# - Modules and files: lowercase_with_underscores (e.g., value_per_mile.py)
# - Functions: lowercase_with_underscores (e.g., get_value_per_mile_airlines)
# - Variables: lowercase_with_underscores (e.g., total_distance)
# - Classes: CapitalizedWords (e.g., ValuePerMile)
# - Constants: ALL_UPPERCASE_WITH_UNDERSCORES (e.g., ORIGIN)
def create_route_object(route_type, carrier, price, miles, class_code="Y"):
    if route_type == "flight":
        vpm = get_value_per_mile_airlines(carrier, class_code)
    elif route_type == "gift_card":
        vpm = value_per_mile_giftCards(carrier)
    elif route_type == "hotel":
        vpm = value_per_mile_hotels(carrier)
    return {
        "type": route_type,
        "airline": carrier,
        "route": [route_type.upper()],
        "total_distance": miles,
        "price": price,
        "vpm": round(vpm, 2) if vpm else 0
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
    return sorted(routes, key=key, reverse=reverse)[:3]

def gather_all_routes():
    flight_routes = []
    direct_flight = get_roundtrip(Origin, Destination, Departure_Date, Return_Date)
    direct_price = float(direct_flight["price_details"]["display_total_fare"])

    try:
        direct_out = one_way(Origin, Destination, Departure_Date)[0]
        direct_in = one_way(Destination, Origin, Return_Date)[0]
        flight_routes.append(create_route_object("flight", direct_out["airline"], direct_out["price"], 2200))
        flight_routes.append(create_route_object("flight", direct_in["airline"], direct_in["price"], 2200))
    except:
        pass

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

    if valid_out and valid_in:
        best_out = min(valid_out, key=lambda x: x["price"])
        best_in = min(valid_in, key=lambda x: x["price"])
        flight_routes.append(create_route_object("flight", best_out["leg1"]["airline"], best_out["leg1"]["price"], 1100))
        flight_routes.append(create_route_object("flight", best_out["leg2"]["airline"], best_out["leg2"]["price"], 1100))
        flight_routes.append(create_route_object("flight", best_in["leg1"]["airline"], best_in["leg1"]["price"], 1100))
        flight_routes.append(create_route_object("flight", best_in["leg2"]["airline"], best_in["leg2"]["price"], 1100))

    gift_card_routes = [
        create_route_object("gift_card", "DL", 100, 300),
        create_route_object("gift_card", "UA", 120, 300)
    ]

    hotel_routes = [
        create_route_object("hotel", "AA", 90, 300),
        create_route_object("hotel", "DL", 160, 400)
    ]

    return flight_routes + gift_card_routes + hotel_routes

def display_recommendations(routes, priority):
    print(f"\nTop 3 redemption options by '{priority}':\n")
    for i, route in enumerate(routes, 1):
        print(f"{i}. {route['type'].upper()} | {route['airline']} | "
              f"Price: ${route['price']} | Distance: {route['total_distance']} mi | "
              f"VPM: {route['vpm']}¢/mile")

priority = "value_per_mile"
all_routes = gather_all_routes()
top_choices = recommend_routes(all_routes, priority)
display_recommendations(top_choices, priority)
