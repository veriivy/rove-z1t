import { NextRequest, NextResponse } from 'next/server';

interface FlightRoute {
  type: string;
  airline: string;
  price: number;
  total_distance: number;
  vpm: number;
  synthetic?: boolean;
  roundtrip?: boolean;
  legs?: Array<{
    airline: string;
    price: number;
    departure: string;
    arrival: string;
    origin: string;
    destination: string;
  }>;
}

interface SearchParams {
  origin: string;
  destination: string;
  departureDate: string;
  returnDate: string;
  passengers: string;
  cabinClass: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: SearchParams = await request.json();
    
    // Validate input
    if (!body.origin || !body.destination || !body.departureDate || !body.returnDate) {
      return NextResponse.json(
        { error: 'Missing required parameters' },
        { status: 400 }
      );
    }

    // Call your Python backend
    const pythonResponse = await fetch('http://localhost:5000/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        origin: body.origin,
        destination: body.destination,
        departure_date: body.departureDate,
        return_date: body.returnDate,
        class: body.cabinClass === 'economy' ? 'Y' : 
               body.cabinClass === 'premium_economy' ? 'W' : 
               body.cabinClass === 'business' ? 'J' : 'Y',
        priority: 'value_per_mile'
      }),
    });

    if (!pythonResponse.ok) {
      throw new Error(`Python backend error: ${pythonResponse.status}`);
    }

    const pythonData = await pythonResponse.json();
    
    // Transform the Python backend response to match frontend expectations
    const transformedData = {
      outbound: [],
      inbound: [],
      misc: [],
      details: pythonData.details || ''
    };
    
    // Transform outbound flights
    if (pythonData.outbound) {
      transformedData.outbound = pythonData.outbound.map((route: any) => ({
        type: route.synthetic ? 'SYN FLIGHT' : route.roundtrip ? 'RT FLIGHT' : 'DIR FLIGHT',
        airline: route.airline,
        price: route.price,
        distance: route.total_distance,
        vpm: route.vpm,
        legs: route.legs
      }));
    }
    
    // Transform inbound flights
    if (pythonData.inbound) {
      transformedData.inbound = pythonData.inbound.map((route: any) => ({
        type: route.synthetic ? 'SYN FLIGHT' : route.roundtrip ? 'RT FLIGHT' : 'DIR FLIGHT',
        airline: route.airline,
        price: route.price,
        distance: route.total_distance,
        vpm: route.vpm,
        legs: route.legs
      }));
    }
    
    // Transform misc options
    if (pythonData.misc) {
      transformedData.misc = pythonData.misc.map((route: any) => ({
        type: route.type.toUpperCase(),
        airline: route.airline,
        price: route.price,
        distance: route.total_distance,
        vpm: route.vpm
      }));
    }

    return NextResponse.json(transformedData);

  } catch (error) {
    console.error('Error calling Python backend:', error);
    return NextResponse.json(
      { error: 'Failed to get recommendations from Python backend' },
      { status: 500 }
    );
  }
} 