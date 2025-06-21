import requests
from datetime import datetime, timedelta

AIRLINES_WHITELIST = {"UA", "DL","AA"}

def get_data(dep_date,ret_date):
	url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip"
	
	querystring = {"sid":"iSiX639",
                	"origin_airport_code":"MIA,JFK",
                    "adults":"1",
                    "departure_date":f"{dep_date},{ret_date}",
                    "destination_airport_code":"JFK,YWG"}

	headers = {
	"x-rapidapi-key": "4b5cfb9794msha65a207bf711a16p12910cjsn642f80d40472",
	"x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	return response.json()
start_date = datetime(2025, 6, 21).date()
end_date = datetime(2025, 6, 25).date()
trip_length = 4  # days between departure and return
current_date = start_date
while current_date <= end_date:
    return_date = current_date + timedelta(days=trip_length)
    data = get_data(current_date, return_date)

    if "error" in data["getAirFlightRoundTrip"]:
        current_date += timedelta(days=1)
        continue

    itineraries = data["getAirFlightRoundTrip"]["results"]["result"]["itinerary_data"]
    
    for itin_key, itin in itineraries.items():
        price = itin["price_details"]["display_total_fare"]
        slices = itin["slice_data"]

        outbound_airline = slices["slice_0"]["airline"]["code"]
        return_airline = slices["slice_1"]["airline"]["code"]

        # Filter airlines
        if outbound_airline not in AIRLINES_WHITELIST and return_airline not in AIRLINES_WHITELIST:
            continue

        dep_time = slices["slice_0"]["departure"]["datetime"]["date_time"]
        ret_time = slices["slice_1"]["departure"]["datetime"]["date_time"]
        dep_str = datetime.fromisoformat(dep_time).strftime("%a, %b %d at %#I:%M %p")
        ret_str = datetime.fromisoformat(ret_time).strftime("%a, %b %d at %#I:%M %p")

        print(f"{current_date} → {return_date} | Airline: {outbound_airline}/{return_airline} | Price: ${price} | Out: {dep_str} | Back: {ret_str}")

    current_date += timedelta(days=1)
