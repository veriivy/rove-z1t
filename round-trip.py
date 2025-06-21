import http.client

conn = http.client.HTTPSConnection("priceline-com-provider.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "ae154958cbmsh0156f277de1e385p171d11jsnbd9a365120e3",
    'x-rapidapi-host': "priceline-com-provider.p.rapidapi.com"
}

conn.request("GET", "/v2/flight/roundTrip?sid=iSiX639&origin_airport_code=YWG%2CJFK&adults=1&departure_date=2021-12-21%2C2021-12-25&destination_airport_code=JFK%2CYWG", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
