# Flight Recommendation Tool

A Next.js web application that recommends flight routes based on value per mile, price, and distance. This tool uses your actual Python code for flight routing and synthetic routing algorithms.

## Architecture

This application uses a **two-server architecture**:

- **Frontend**: Next.js web application (port 3000)
- **Backend**: Python Flask server running your existing code (port 5000)

The Next.js app calls your Python backend API to get real flight recommendations using your existing logic.

## Features

- **Flight Search**: Search for flights by origin, destination, dates, and class
- **Multiple Priority Options**: Sort recommendations by value per mile, price, or distance
- **Route Types**: Supports direct flights, roundtrip flights, and synthetic routes (connecting flights)
- **Value per Mile Analysis**: Calculates and displays value per mile for different airlines and classes
- **Alternative Redemptions**: Shows gift card and hotel redemption options
- **Responsive Design**: Modern, mobile-friendly interface

## Route Types

- **DIR**: Direct flights
- **RT**: Roundtrip flights
- **SYN**: Synthetic routes (connecting flights through hubs)

## Airlines Supported

- **AA**: American Airlines
- **UA**: United Airlines  
- **DL**: Delta Airlines
- **MULTI**: Multi-airline synthetic routes

## Class Options

- **Y**: Economy Class
- **W**: Premium Economy
- **J**: Business/First Class

## Priority Options

- **Value per Mile**: Optimizes for maximum value per mile
- **Price**: Finds the cheapest options
- **Distance**: Prioritizes shorter routes

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+ 
- npm or yarn

### Quick Start

1. **Start both servers with one command**:
   ```bash
   python start_servers.py
   ```

   This will:
   - Install Python dependencies
   - Start the Python Flask backend (port 5000)
   - Install Node.js dependencies
   - Start the Next.js frontend (port 3000)

2. **Open your browser**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Manual Start

If you prefer to start servers manually:

1. **Start Python Backend**:
   ```bash
   pip install -r requirements.txt
   python python_backend.py
   ```

2. **Start Next.js Frontend** (in a new terminal):
   ```bash
   cd flight-recommendation-tool
   npm install
   npm run dev
   ```

## Usage

1. **Enter Flight Details**:
   - Origin airport code (e.g., IST)
   - Destination airport code (e.g., JFK)
   - Departure date
   - Return date
   - Class of service
   - Priority for recommendations

2. **Search Flights**: Click "Search Flights" to get recommendations

3. **Review Results**: The app will display:
   - Top 3 outbound flight options
   - Top 3 inbound flight options  
   - Other redemption options (gift cards, hotels)

## How It Works

1. **User Input**: Enter flight details in the Next.js frontend
2. **API Call**: Frontend sends request to `/api/recommendations`
3. **Python Backend**: Next.js calls your Python Flask server
4. **Your Python Code**: Flask server runs your existing `final_recommendation_tool.py` logic
5. **Real API Calls**: Your Python code calls the Priceline API for real flight data
6. **Results**: Python returns processed recommendations to Next.js
7. **Display**: Next.js displays the results in a beautiful web interface

## Python Backend API

The Python Flask server exposes these endpoints:

- `POST /recommendations` - Get flight recommendations
- `GET /health` - Health check

### Request Format
```json
{
  "origin": "IST",
  "destination": "JFK",
  "departure_date": "2025-07-23",
  "return_date": "2025-07-26",
  "class": "Y",
  "priority": "value_per_mile"
}
```

## Value per Mile Calculations

The tool uses your exact Python VPM logic:

### American Airlines (AA)
- Economy: 1.6¢/mile
- Premium Economy: 1.92¢/mile  
- Business/First: 3.3¢/mile

### United Airlines (UA)
- Economy: 1.09¢/mile
- Premium Economy: 1.32¢/mile
- Business/First: 1.46¢/mile

### Delta Airlines (DL)
- Economy: 1.12¢/mile
- Business: 1.24¢/mile
- Premium Business: 1.22¢/mile
- First Class: 1.10¢/mile

## Technology Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Python Flask, your existing flight recommendation logic
- **APIs**: Priceline API (via your Python code)
- **Data**: Real flight data from Priceline API

## Project Structure

```
rove-z1t/
├── python_backend.py          # Flask server wrapping your Python code
├── requirements.txt           # Python dependencies
├── start_servers.py          # Script to start both servers
├── final_recommendation_tool.py  # Your existing Python logic
├── final_synthetic_routing.py    # Your existing routing logic
├── value_per_mile.py         # Your VPM calculations
├── flights.db                # Your flight database
└── flight-recommendation-tool/   # Next.js frontend
    ├── src/app/
    │   ├── api/recommendations/route.ts  # API route calling Python backend
    │   └── page.tsx                      # Main frontend page
    └── package.json
```

## Development

### Available Scripts

- `python start_servers.py` - Start both servers
- `python python_backend.py` - Start Python backend only
- `cd flight-recommendation-tool && npm run dev` - Start Next.js frontend only

## Future Enhancements

- Integration with additional flight APIs
- User authentication and saved searches
- Advanced filtering options
- Real-time flight availability
- Email notifications for price drops
- Mobile app version

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.