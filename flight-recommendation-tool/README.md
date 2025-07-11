# Flight Recommendation Tool

A Next.js web application that recommends flight routes based on value per mile, price, and distance. This tool is based on Python logic for flight routing and synthetic routing algorithms.

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

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the project directory:
```bash
cd flight-recommendation-tool
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

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

## API Integration

The application includes an API route at `/api/recommendations` that accepts POST requests with flight search parameters and returns sorted recommendations.

### API Endpoint

```
POST /api/recommendations
```

### Request Body

```json
{
  "origin": "IST",
  "destination": "JFK", 
  "departureDate": "2025-07-23",
  "returnDate": "2025-07-26",
  "class": "Y",
  "priority": "value_per_mile"
}
```

### Response Format

```json
{
  "outbound": [
    {
      "type": "flight",
      "airline": "AA",
      "price": 850.00,
      "total_distance": 2200,
      "vpm": 1.6,
      "roundtrip": true,
      "legs": [...]
    }
  ],
  "inbound": [...],
  "misc": [...]
}
```

## Value per Mile Calculations

The tool calculates value per mile based on airline and class:

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

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Date Handling**: date-fns
- **HTTP Client**: Built-in fetch API

## Development

### Project Structure

```
src/
├── app/
│   ├── api/
│   │   └── recommendations/
│   │       └── route.ts          # API endpoint
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main page component
```

### Available Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint

## Future Enhancements

- Integration with real flight APIs (Priceline, etc.)
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
