import requests
ORIGIN = "LAX"
DESTINATION = "JFK"
HUBS = ["ATL", "CLT", "ORD", "DFW", "BOS", "PHL", "YYZ", "YUL"]
AIRLINES_WHITELIST = {"UA", "DL", "AA"}

DEPARTURE_DATE = "2025-06-28"
RETURN_DATE = "2025-06-30"

HEADERS = {
    "x-rapidapi-key": "4b5cfb9794msha65a207bf711a16p12910cjsn642f80d40472",
    "x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
}

url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/departures"
params = {"departure_date":"2025-06-29",
              "sid":"iSiX639",
              "origin_airport_code":"LAX",
              "destination_airport_code":"ATL",
              "adults":"1"}

res = requests.get(url, headers=HEADERS, params=params).json()
itineraries = res["getAirFlightDepartures"]["results"]["result"]["itinerary_data"]
for itin in itineraries.values():
            airline = itin["slice_data"]["slice_0"]["airline"]["code"]
            if airline in AIRLINES_WHITELIST:
                print(float(itin["price_details"]["display_total_fare"]))