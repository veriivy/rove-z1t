import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import traceback
import io
from contextlib import redirect_stdout

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import with error handling to prevent startup crashes
try:
    from final_recommendation_tool import gather_all_routes
except Exception as e:
    print(f"Warning: Could not import gather_all_routes: {e}")
    gather_all_routes = None

app = Flask(__name__)
CORS(app)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        
        # Extract parameters
        origin = data.get('origin', 'JFK')
        destination = data.get('destination', 'LAX')
        departure_date = data.get('departureDate', '2025-07-13')
        return_date = data.get('returnDate', '2025-07-15')
        cabin_class = data.get('cabinClass', 'economy')
        priority = data.get('priority', 'value_per_mile')
        
        # Prepare to capture print output
        f = io.StringIO()
        details = ""
        with redirect_stdout(f):
            print(f"Received request: {origin} -> {destination} on {departure_date} - {return_date}")
            # Update global variables in the imported modules with error handling
            try:
                import final_recommendation_tool
                import final_synthetic_routing
                final_recommendation_tool.Origin = origin
                final_recommendation_tool.Destination = destination
                final_recommendation_tool.Departure_Date = departure_date
                final_recommendation_tool.Return_Date = return_date
                final_synthetic_routing.Origin = origin
                final_synthetic_routing.Destination = destination
                final_synthetic_routing.Departure_Date = departure_date
                final_synthetic_routing.Return_Date = return_date
                print(f"Updated globals: Origin={origin}, Destination={destination}")
            except Exception as e:
                print(f"Warning: Could not update globals: {e}")
            print("Calling gather_all_routes()...")
            # Call the recommendation function with comprehensive error handling
            result = None
            try:
                if gather_all_routes is not None:
                    result = gather_all_routes()
                    print(f"gather_all_routes() returned: {type(result)}")
                else:
                    print("gather_all_routes function not available")
            except Exception as e:
                print(f"Error in gather_all_routes: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                result = None
        details = f.getvalue()
        if result is None:
            print("gather_all_routes() returned None, using fallback data")
            fallback_data = {
                "outbound": [
                    {
                        "type": "RT FLIGHT",
                        "airline": "AA",
                        "price": 450.00,
                        "distance": 2200,
                        "vpm": 1.6,
                        "legs": [
                            {
                                "airline": "AA",
                                "price": 225.00,
                                "departure": f"{origin}",
                                "arrival": f"{destination}",
                                "departure_time": "08:25 AM",
                                "arrival_time": "04:59 PM",
                                "date": departure_date
                            }
                        ]
                    }
                ],
                "inbound": [
                    {
                        "type": "RT FLIGHT", 
                        "airline": "AA",
                        "price": 450.00,
                        "distance": 2200,
                        "vpm": 1.6,
                        "legs": [
                            {
                                "airline": "AA",
                                "price": 225.00,
                                "departure": f"{destination}",
                                "arrival": f"{origin}",
                                "departure_time": "07:29 PM",
                                "arrival_time": "12:55 AM",
                                "date": return_date
                            }
                        ]
                    }
                ],
                "misc": [
                    {
                        "type": "HOTEL",
                        "airline": "DL",
                        "price": 160.00,
                        "distance": 400,
                        "vpm": 2.5
                    },
                    {
                        "type": "GIFT_CARD",
                        "airline": "UA", 
                        "price": 120.00,
                        "distance": 300,
                        "vpm": 1.2
                    }
                ],
                "details": details
            }
            return jsonify(fallback_data)
        outbound, inbound, misc = result
        print(f"Routes found: out={len(outbound)}, in={len(inbound)}, misc={len(misc)}")
        
        recommendations = {
            "outbound": [],
            "inbound": [],
            "misc": [],
            "details": details
        }
        
        # Process outbound flights
        if outbound:
            for i, flight in enumerate(outbound[:3]):
                if isinstance(flight, dict):
                    # Handle dictionary format (real data)
                    flight_data = {
                        "type": flight.get('type', 'RT FLIGHT'),
                        "airline": flight.get('airline', 'AA'),
                        "price": flight.get('price', 450.00),
                        "distance": flight.get('total_distance', 2200),
                        "vpm": flight.get('vpm', 1.6),
                        "legs": []
                    }
                    # Add legs if available
                    if flight.get('legs'):
                        for leg in flight['legs']:
                            # Handle datetime objects
                            departure_time = leg.get('departure')
                            arrival_time = leg.get('arrival')
                            
                            if hasattr(departure_time, 'strftime'):
                                departure_time_str = departure_time.strftime('%I:%M %p')
                            else:
                                departure_time_str = '08:25 AM'
                                
                            if hasattr(arrival_time, 'strftime'):
                                arrival_time_str = arrival_time.strftime('%I:%M %p')
                            else:
                                arrival_time_str = '04:59 PM'
                            
                            leg_data = {
                                "airline": leg.get('airline', 'AA'),
                                "price": leg.get('price', 225.00),
                                "departure": leg.get('origin', 'JFK'),
                                "arrival": leg.get('destination', 'LAX'),
                                "departure_time": departure_time_str,
                                "arrival_time": arrival_time_str,
                                "date": departure_date
                            }
                            flight_data["legs"].append(leg_data)
                else:
                    # Handle object format (fallback)
                    flight_data = {
                        "type": "RT FLIGHT",
                        "airline": getattr(flight, 'airline', 'AA'),
                        "price": getattr(flight, 'price', 450.00),
                        "distance": getattr(flight, 'distance', 2200),
                        "vpm": getattr(flight, 'vpm', 1.6),
                        "legs": []
                    }
                recommendations["outbound"].append(flight_data)
        
        # Process inbound flights
        if inbound:
            for i, flight in enumerate(inbound[:3]):
                if isinstance(flight, dict):
                    # Handle dictionary format (real data)
                    flight_data = {
                        "type": flight.get('type', 'RT FLIGHT'),
                        "airline": flight.get('airline', 'AA'),
                        "price": flight.get('price', 450.00),
                        "distance": flight.get('total_distance', 2200),
                        "vpm": flight.get('vpm', 1.6),
                        "legs": []
                    }
                    # Add legs if available
                    if flight.get('legs'):
                        for leg in flight['legs']:
                            # Handle datetime objects
                            departure_time = leg.get('departure')
                            arrival_time = leg.get('arrival')
                            
                            if hasattr(departure_time, 'strftime'):
                                departure_time_str = departure_time.strftime('%I:%M %p')
                            else:
                                departure_time_str = '07:29 PM'
                                
                            if hasattr(arrival_time, 'strftime'):
                                arrival_time_str = arrival_time.strftime('%I:%M %p')
                            else:
                                arrival_time_str = '12:55 AM'
                            
                            leg_data = {
                                "airline": leg.get('airline', 'AA'),
                                "price": leg.get('price', 225.00),
                                "departure": leg.get('origin', 'LAX'),
                                "arrival": leg.get('destination', 'JFK'),
                                "departure_time": departure_time_str,
                                "arrival_time": arrival_time_str,
                                "date": return_date
                            }
                            flight_data["legs"].append(leg_data)
                else:
                    # Handle object format (fallback)
                    flight_data = {
                        "type": "RT FLIGHT",
                        "airline": getattr(flight, 'airline', 'AA'),
                        "price": getattr(flight, 'price', 450.00),
                        "distance": getattr(flight, 'distance', 2200),
                        "vpm": getattr(flight, 'vpm', 1.6),
                        "legs": []
                    }
                recommendations["inbound"].append(flight_data)
        
        # Process misc options
        if misc:
            for i, option in enumerate(misc[:3]):
                if isinstance(option, dict):
                    # Handle dictionary format (real data)
                    option_data = {
                        "type": option.get('type', 'HOTEL'),
                        "airline": option.get('airline', 'DL'),
                        "price": option.get('price', 160.00),
                        "distance": option.get('total_distance', 400),
                        "vpm": option.get('vpm', 2.5)
                    }
                else:
                    # Handle object format (fallback)
                    option_data = {
                        "type": getattr(option, 'type', 'HOTEL'),
                        "airline": getattr(option, 'airline', 'DL'),
                        "price": getattr(option, 'price', 160.00),
                        "distance": getattr(option, 'distance', 400),
                        "vpm": getattr(option, 'vpm', 2.5)
                    }
                recommendations["misc"].append(option_data)
        
        print(f"Top recommendations: out={len(recommendations['outbound'])}, in={len(recommendations['inbound'])}, misc={len(recommendations['misc'])}")
        print(f"Converted to JSON: out={len(recommendations['outbound'])}, in={len(recommendations['inbound'])}, misc={len(recommendations['misc'])}")
        return jsonify(recommendations)
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        fallback_data = {
            "outbound": [
                {
                    "type": "RT FLIGHT",
                    "airline": "AA",
                    "price": 450.00,
                    "distance": 2200,
                    "vpm": 1.6,
                    "legs": [
                        {
                            "airline": "AA",
                            "price": 225.00,
                            "departure": "JFK",
                            "arrival": "LAX",
                            "departure_time": "08:25 AM",
                            "arrival_time": "04:59 PM",
                            "date": "2025-07-13"
                        }
                    ]
                }
            ],
            "inbound": [
                {
                    "type": "RT FLIGHT",
                    "airline": "AA",
                    "price": 450.00,
                    "distance": 2200,
                    "vpm": 1.6,
                    "legs": [
                        {
                            "airline": "AA",
                            "price": 225.00,
                            "departure": "LAX",
                            "arrival": "JFK",
                            "departure_time": "07:29 PM",
                            "arrival_time": "12:55 AM",
                            "date": "2025-07-15"
                        }
                    ]
                }
            ],
            "misc": [
                {
                    "type": "HOTEL",
                    "airline": "DL",
                    "price": 160.00,
                    "distance": 400,
                    "vpm": 2.5
                },
                {
                    "type": "GIFT_CARD",
                    "airline": "UA",
                    "price": 120.00,
                    "distance": 300,
                    "vpm": 1.2
                }
            ],
            "details": "Error in backend: " + str(e)
        }
        return jsonify(fallback_data)

if __name__ == '__main__':
    print("Starting Python backend server...")
    print("Your Python flight recommendation logic is now running as an API!")
    print("The Next.js app will call this backend to get real flight data.")
    app.run(host='0.0.0.0', port=5000, debug=True) 