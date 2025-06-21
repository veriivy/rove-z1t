import requests

url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/roundTrip"

querystring = {"sid":"iSiX639","origin_airport_code":"YWG,JFK","adults":"1","departure_date":"2021-12-21,2021-12-25","destination_airport_code":"JFK,YWG"}

headers = {"x-rapidapi-host": "priceline-com-provider.p.rapidapi.com"}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
