from typing import List, Dict

#example of expected route data:
# data = [
#     {
#         "airline": "United",
#         "route": ["SFO", "ORD", "JFK"],
#         "total_distance": 2800,
#         "price": 290,
#         "vpm": 7.3
#     }
# ]

def recommend_routes(routes: List[Dict], priority: str) -> List[Dict]:
    if priority not in {"distance", "value_per_mile", "price"}:
        raise ValueError("Priority must be one of: 'distance', 'value_per_mile', 'price'")

    # You can choose to be recommended based on flight distance, vpm, or overall route price
    if priority == "distance":
        sort_key = lambda r: r["total_distance"]
        reverse = False
    elif priority == "value_per_mile":
        sort_key = lambda r: r["vpm"]  
        reverse = True
    elif priority == "price":
        sort_key = lambda r: r["price"] 
        reverse = False

    # returns the top three in the sorted list

    sorted_routes = sorted(routes, key=sort_key, reverse=reverse)
    return sorted_routes[:3]

# example implementatoin: displays the top 3 best options in the data

# priority_choice = "value_per_mile"
# top_routes = recommend_routes(data, priority_choice)

# print(f"Top 3 routes by {priority_choice}:")
# for i, route in enumerate(top_routes, 1):
#     print(f"{i}. Airline: {route['airline']}, Route: {' → '.join(route['route'])}, "
#           f"Distance: {route['total_distance']} mi, Price: ${route['price']}, VPM: {route['vpm']}")
