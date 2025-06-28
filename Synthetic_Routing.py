import requests
from datetime import datetime, timedelta

#set-up
Origin = "MIA"
Destination = "JFK"
Hubs = ["ATL", "CLT", "ORD", "DFW", "BOS", "PHL"]
Airline_Whitelist = {"F9"}
min_layover = timedelta(minutes=75)

Departure_Date = "2025-07-23"
Return_Date = "2025-07-26"

Headers = {
    "x-rapidapi-key": "81a303ed3bmsh2517e839f327728p19d220jsn9b336344227d",
    "x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
}
#direct one-way flight
def one_way(origin, destination, date):
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
    params = {"departure_date":date,
              "sid":"iSiX639",
              "origin_airport_code":origin,
              "destination_airport_code":destination,
              "adults":"1"}
    res = requests.get(url, headers=Headers, params=params).json()
    itineraries = res["getAirFlightDepartures"]["results"]["result"]["itinerary_data"]
    direct = []
    for itin in itineraries.values():
            airline = itin["slice_data"]["slice_0"]["airline"]["code"]
            if airline not in Airline_Whitelist:
                continue

            details = itin["slice_data"]["slice_0"]
            dep = datetime.fromisoformat(details["departure"]["datetime"]["date_time"])
            arr = datetime.fromisoformat(details["arrival"]["datetime"]["date_time"])
            fare = float(itin["price_details"]["display_total_fare"])
            direct.append({
                "airline": airline,
                "price": fare,
                "departure": dep,
                "arrival": arr
            })
            break
    return direct
#all possible one-way flights
def get_oneway_options(origin, destination, date):
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
    params = {"departure_date":date,
              "sid":"iSiX639",
              "origin_airport_code":origin,
              "destination_airport_code":destination,
              "adults":"1"}
    res = requests.get(url, headers=Headers, params=params).json()
    itineraries = res["getAirFlightDepartures"]["results"]["result"]["itinerary_data"]
    options = []
    for itin in itineraries.values():
            airline = itin["slice_data"]["slice_0"]["airline"]["code"]
            if airline not in Airline_Whitelist:
                continue

            details = itin["slice_data"]["slice_0"]
            dep = datetime.fromisoformat(details["departure"]["datetime"]["date_time"])
            arr = datetime.fromisoformat(details["arrival"]["datetime"]["date_time"])
            fare = float(itin["price_details"]["display_total_fare"])
            options.append({
                "airline": airline,
                "price": fare,
                "departure": dep,
                "arrival": arr
            })
    return options

#round-trip
def get_roundtrip(origin, destination, dep_date, ret_date):
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip"
    params = {
        "sid": "iSiX639",
        "origin_airport_code": f"{origin},{destination}",
        "adults": "1",
        "departure_date": f"{dep_date},{ret_date}",
        "destination_airport_code": f"{destination},{origin}"
        
    }

    res = requests.get(url, headers=Headers, params=params).json()
    itineraries = res["getAirFlightRoundTrip"]["results"]["result"]["itinerary_data"]
    for itin in itineraries.values():
            slices = itin["slice_data"]
            out_airline = slices["slice_0"]["airline"]["code"]
            ret_airline = slices["slice_1"]["airline"]["code"]
            if out_airline in Airline_Whitelist or ret_airline in Airline_Whitelist:
                return itin
#make sure people have enough time between connecting flights
def valid_layover(leg1_options, leg2_options,hub):
    valid_pairs = []
    for leg1 in leg1_options:
        for leg2 in leg2_options:
            if leg2["departure"] > leg1["arrival"] + min_layover:
                total_price = leg1["price"] + leg2["price"]
                valid_pairs.append({
                    "hub": hub,
                    "price": total_price,
                    "leg1": leg1,
                    "leg2": leg2
                })
    if valid_pairs:
        return min(valid_pairs, key=lambda x: x["price"])
    else:
        return None
    
def print_leg_details(label, leg):
    dep_time = leg["departure"].strftime("%a, %b %d at %#I:%M %p")
    arr_time = leg["arrival"].strftime("%a, %b %d at %#I:%M %p")
    print(f"{label}: {leg['airline']} | ${leg['price']} | Departs {dep_time} → Arrives {arr_time}")

def print_direct_details(flight):
    price = flight["price_details"]["display_total_fare"]
    out_slice = flight["slice_data"]["slice_0"]
    ret_slice = flight["slice_data"]["slice_1"]

    out_dep = datetime.fromisoformat(out_slice["departure"]["datetime"]["date_time"])
    out_arr = datetime.fromisoformat(out_slice["arrival"]["datetime"]["date_time"])
    ret_dep = datetime.fromisoformat(ret_slice["departure"]["datetime"]["date_time"])
    ret_arr = datetime.fromisoformat(ret_slice["arrival"]["datetime"]["date_time"])

    out_airline = out_slice["airline"]["code"]
    ret_airline = ret_slice["airline"]["code"]

    print("\nDirect roundtrip flight details:")
    print(f"Total Price: ${price}")
    print(f"Outbound: {out_airline} | Departs {out_dep.strftime('%a, %b %d at %#I:%M %p')} → Arrives {out_arr.strftime('%a, %b %d at %#I:%M %p')}")
    print(f"Inbound: {ret_airline} | Departs {ret_dep.strftime('%a, %b %d at %#I:%M %p')} → Arrives {ret_arr.strftime('%a, %b %d at %#I:%M %p')}")

#get direct price
direct_flight = get_roundtrip(Origin, Destination, Departure_Date, Return_Date)
price = direct_flight["price_details"]["display_total_fare"]
valid_out = []
valid_in = []
#find best synthetic prices
for hub in Hubs:
    if hub in [Origin, Destination]:
        continue

    leg1_options = get_oneway_options(Origin, hub, Departure_Date)
    leg2_options = get_oneway_options(hub, Destination, Departure_Date)
    current = valid_layover(leg1_options,leg2_options,hub)
    if current:
        valid_out.append(current)

    leg3_options = get_oneway_options(Destination, hub, Return_Date)
    leg4_options = get_oneway_options(hub,Origin, Return_Date)
    current = valid_layover(leg3_options,leg4_options,hub)
    if current:
        valid_in.append(current)
#compare
total = price + 1
if valid_out and valid_in:
    best_out = min(valid_out, key=lambda x: x["price"])
    cheap_out = best_out
    direct_out = one_way(Origin, Destination, Departure_Date)[0]
    if best_out['price'] > direct_out['price']:
        cheap_out = direct_out
    best_in = min(valid_in, key=lambda x: x["price"])
    cheap_in = best_in
    direct_in = one_way(Destination, Origin, Return_Date)[0]
    if best_in['price']> direct_in['price']:
        cheap_in = direct_in
    total = cheap_in['price']+cheap_out['price']
else:
    print("No synthetic route available.")
if total<price:
    print("Synthetic saves you money")
    print("\nBest outbound synthetic route:")
    print(f"Through hub: {best_out['hub']} | Total: ${best_out['price']}")
    print_leg_details(f"Leg 1 ({Origin} → {best_out['hub']})", best_out["leg1"])
    print_leg_details(f"Leg 2 ({best_out['hub']} → {Destination})", best_out["leg2"])
     
    print("\nBest inbound synthetic route:")
    print(f"Through hub: {best_in['hub']} | Total: ${best_in['price']}")
    print_leg_details(f"Leg 1 ({Destination} → {best_in['hub']})", best_in["leg1"])
    print_leg_details(f"Leg 2 ({best_in['hub']} → {Origin})", best_in["leg2"])
elif total>price:
    print("Direct is the best way")
    print_direct_details(direct_flight)
else:
    print("Both methods cost the same")
    print("Choose what you'd prefer")

    print_direct_details(direct_flight)

    print("\nBest outbound synthetic route:")
    print(f"Through hub: {best_out['hub']} | Total: ${best_out['price']}")
    print_leg_details(f"Leg 1 ({Origin} → {best_out['hub']})", best_out["leg1"])
    print_leg_details(f"Leg 2 ({best_out['hub']} → {Destination})", best_out["leg2"])
     
    print("\nBest inbound synthetic route:")
    print(f"Through hub: {best_in['hub']} | Total: ${best_in['price']}")
    print_leg_details(f"Leg 1 ({Destination} → {best_in['hub']})", best_in["leg1"])
    print_leg_details(f"Leg 2 ({best_in['hub']} → {Origin})", best_in["leg2"])

