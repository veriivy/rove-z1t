import requests

headers = {
    "x-rapidapi-key": "af7df56d80msh53e556cad1a285bp149b79jsn9d83ff4400b1",
    "x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"
}

url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip"
params = {
    "number_of_itineraries": "10",
    "sid": "iSiX639",
    "origin_airport_code": "JFK,LAX",
    "adults": "1",
    "departure_date": "2025-07-13,2025-07-15",
    "destination_airport_code": "LAX,JFK"
}

try:
    res = requests.get(url, headers=headers, params=params).json()
    print("API Response keys:", list(res.keys()))
    
    if "getAirFlightRoundTrip" in res:
        roundtrip = res["getAirFlightRoundTrip"]
        print("getAirFlightRoundTrip keys:", list(roundtrip.keys()))
        
        if "results" in roundtrip:
            results = roundtrip["results"]
            print("results keys:", list(results.keys()))
            
            if "result" in results:
                result = results["result"]
                print("result keys:", list(result.keys()))
                
                if "itinerary_data" in result:
                    itinerary_data = result["itinerary_data"]
                    print("itinerary_data keys:", list(itinerary_data.keys()))
                    print("Number of itineraries:", len(itinerary_data))
                    
                    # Check first itinerary structure
                    if itinerary_data:
                        first_key = list(itinerary_data.keys())[0]
                        first_itinerary = itinerary_data[first_key]
                        print("First itinerary keys:", list(first_itinerary.keys()))
                        
                        if "slice_data" in first_itinerary:
                            slice_data = first_itinerary["slice_data"]
                            print("slice_data keys:", list(slice_data.keys()))
                else:
                    print("No itinerary_data in result")
            else:
                print("No result in results")
        else:
            print("No results in getAirFlightRoundTrip")
    else:
        print("No getAirFlightRoundTrip in response")
        
except Exception as e:
    print(f"Error: {e}") 