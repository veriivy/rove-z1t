import requests
from datetime import datetime, timedelta

#set-up
Origin = "IST"
Destination = "JFK"
Hubs = ["ATL","ORD","DFW"]
Airline_Whitelist = {"AA","UA","DL",}
min_layover = timedelta(minutes=75)

Departure_Date = "2025-07-23"
Return_Date = "2025-07-26"

Headers = {
    "x-rapidapi-key": "af7df56d80msh53e556cad1a285bp149b79jsn9d83ff4400b1",
    "x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
}

#direct one-way flight
def one_way(origin, destination, date):
    try:
        url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
        params = {
            "departure_date": date,
            "sid": "iSiX639",
            "origin_airport_code": origin,
            "destination_airport_code": destination,
            "adults": "1",
            "number_of_itineraries": "10"
        }
        res = requests.get(url, headers=Headers, params=params).json()
        
        # Debug: Print the actual response structure
        print(f"API Response keys: {list(res.keys())}")
        if "getAirFlightDepartures" not in res:
            print(f"Available keys: {list(res.keys())}")
            return []
            
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
    except Exception as e:
        print(f"Error in one_way: {e}")
        return []

#all possible one-way flights
def get_oneway_options(origin, destination, date):
    try:
        url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
        params = {
            "departure_date": date,
            "sid": "iSiX639",
            "origin_airport_code": origin,
            "destination_airport_code": destination,
            "adults": "1",
            "number_of_itineraries": "10"
        }
        res = requests.get(url, headers=Headers, params=params).json()
        
        # Debug: Print the actual response structure
        print(f"get_oneway_options API Response keys: {list(res.keys())}")
        if "getAirFlightDepartures" not in res:
            print(f"Available keys: {list(res.keys())}")
            return []
            
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
    except Exception as e:
        print(f"Error in get_oneway_options: {e}")
        return []

#round-trip
def get_roundtrip(origin, destination, dep_date, ret_date):
    try:
        url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip"
        params = {
            "number_of_itineraries": "10",
            "sid": "iSiX639",
            "origin_airport_code": f"{origin},{destination}",
            "adults": "1",
            "departure_date": f"{dep_date},{ret_date}",
            "destination_airport_code": f"{destination},{origin}"
            
        }

        res = requests.get(url, headers=Headers, params=params).json()
        
        # Debug: Print the actual response structure
        print(f"get_roundtrip API Response keys: {list(res.keys())}")
        if "getAirFlightRoundTrip" not in res:
            print(f"Available keys: {list(res.keys())}")
            return None
            
        itineraries = res["getAirFlightRoundTrip"]["results"]["result"]["itinerary_data"]
        for itin in itineraries.values():
                slices = itin["slice_data"]
                out_airline = slices["slice_0"]["airline"]["code"]
                ret_airline = slices["slice_1"]["airline"]["code"]
                if out_airline in Airline_Whitelist or ret_airline in Airline_Whitelist:
                    return itin
        return None
    except Exception as e:
        print(f"Error in get_roundtrip: {e}")
        return None

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

