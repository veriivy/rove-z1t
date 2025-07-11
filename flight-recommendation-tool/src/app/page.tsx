'use client';

import { useState } from 'react';
import { Search, Plane, MapPin, Calendar, Users, DollarSign, TrendingUp, Sparkles } from 'lucide-react';

interface FlightRecommendation {
  type: string;
  airline: string;
  price: number;
  distance: number;
  vpm: number;
  legs?: Array<{
    airline: string;
    price: number;
    origin: string;
    destination: string;
    departure: string;
    arrival: string;
  }>;
}

interface Recommendations {
  outbound: FlightRecommendation[];
  inbound: FlightRecommendation[];
  misc: FlightRecommendation[];
  details: string;
}

export default function Home() {
  const [formData, setFormData] = useState({
    origin: '',
    destination: '',
    departureDate: '',
    returnDate: '',
    passengers: '1',
    cabinClass: 'economy'
  });
  const [recommendations, setRecommendations] = useState<Recommendations>({
    outbound: [],
    inbound: [],
    misc: [],
    details: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setRecommendations({ outbound: [], inbound: [], misc: [], details: '' });
    try {
      const response = await fetch('/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }
      const data = await response.json();
      
      // Log the recommendations data to console
      console.log('=== FLIGHT RECOMMENDATIONS DATA ===');
      console.log('Raw API Response:', data);
      console.log('Outbound Flights:', data.outbound || []);
      console.log('Inbound Flights:', data.inbound || []);
      console.log('Misc Options:', data.misc || []);
      console.log('Details:', data.details || '');
      console.log('===================================');
      
      setRecommendations({
        outbound: data.outbound || [],
        inbound: data.inbound || [],
        misc: data.misc || [],
        details: data.details || ''
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getRouteTypeBadge = (type: string) => {
    switch (type) {
      case 'SYN FLIGHT':
        return <span className="badge badge-syn">✨ Synthetic</span>;
      case 'RT FLIGHT':
        return <span className="badge badge-rt">🔄 Roundtrip</span>;
      case 'DIR FLIGHT':
        return <span className="badge badge-dir">✈️ Direct</span>;
      default:
        return <span className="badge badge-dir">✈️ {type}</span>;
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const formatVPM = (vpm: number) => {
    return `${vpm.toFixed(2)}¢/mile`;
  };

  // Inline styles for immediate visual feedback
  const inputStyle = {
    width: '100%',
    padding: '16px',
    border: '2px solid #e5e7eb',
    borderRadius: '12px',
    fontSize: '16px',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    color: '#1f2937', // Dark gray text color
    backdropFilter: 'blur(8px)',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    transition: 'all 0.3s ease',
  };

  const buttonStyle = {
    width: '100%',
    background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
    color: 'white',
    padding: '20px 32px',
    borderRadius: '12px',
    fontSize: '18px',
    fontWeight: 'bold',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    transition: 'all 0.3s ease',
  };

  const cardStyle = {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    backdropFilter: 'blur(12px)',
    borderRadius: '24px',
    padding: '32px',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  };

  const backgroundStyle = {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
    minHeight: '100vh',
    padding: '32px 16px',
  };

  return (
    <div style={backgroundStyle}>
      <div className="min-h-screen py-8 px-4 relative z-10">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="header-container">
            <div className="header-icon">
              <Plane className="h-12 w-12 text-white" />
            </div>
            <h1 className="header-title">Flight Value Finder</h1>
            <p className="header-subtitle">
              Discover the best flight deals with our advanced value-per-mile analysis. 
              Compare airlines and find optimal redemption options for your travel.
            </p>
          </div>

          {/* Search Form */}
          <div style={cardStyle} className="mb-8">
            <h2 className="section-header">
              <Search className="h-8 w-8 text-blue-600" />
              Search Flights
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div>
                  <label className="form-label">
                    <MapPin className="h-5 w-5 text-blue-600" />
                    Origin Airport
                  </label>
                  <input
                    type="text"
                    style={inputStyle}
                    placeholder="Airport code (e.g., JFK)"
                    value={formData.origin}
                    onChange={(e) => setFormData({...formData, origin: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="form-label">
                    <MapPin className="h-5 w-5 text-purple-600" />
                    Destination Airport
                  </label>
                  <input
                    type="text"
                    style={inputStyle}
                    placeholder="Airport code (e.g., LAX)"
                    value={formData.destination}
                    onChange={(e) => setFormData({...formData, destination: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="form-label">
                    <Calendar className="h-5 w-5 text-green-600" />
                    Departure Date
                  </label>
                  <input
                    type="date"
                    style={inputStyle}
                    value={formData.departureDate}
                    onChange={(e) => setFormData({...formData, departureDate: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="form-label">
                    <Calendar className="h-5 w-5 text-orange-600" />
                    Return Date
                  </label>
                  <input
                    type="date"
                    style={inputStyle}
                    value={formData.returnDate}
                    onChange={(e) => setFormData({...formData, returnDate: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="form-label">
                    <Users className="h-5 w-5 text-indigo-600" />
                    Passengers
                  </label>
                  <select
                    style={inputStyle}
                    value={formData.passengers}
                    onChange={(e) => setFormData({...formData, passengers: e.target.value})}
                  >
                    <option value="1">1 Passenger</option>
                    <option value="2">2 Passengers</option>
                    <option value="3">3 Passengers</option>
                    <option value="4">4 Passengers</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">
                    <Plane className="h-5 w-5 text-teal-600" />
                    Cabin Class
                  </label>
                  <select
                    style={inputStyle}
                    value={formData.cabinClass}
                    onChange={(e) => setFormData({...formData, cabinClass: e.target.value})}
                  >
                    <option value="economy">Economy</option>
                    <option value="premium_economy">Premium Economy</option>
                    <option value="business">Business</option>
                    <option value="first">First Class</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                style={buttonStyle}
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-4">
                    <div className="loading-spinner"></div>
                    <span>Finding Best Deals...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-4">
                    <Sparkles className="h-6 w-6" />
                    <span>Search Flights</span>
                  </div>
                )}
              </button>
            </form>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-message">
              <p className="text-red-700 font-semibold">{error}</p>
            </div>
          )}

          {/* Results */}
          {(recommendations.outbound.length > 0 || recommendations.inbound.length > 0 || recommendations.misc.length > 0) && (
            <div className="results-container">
              <div className="flex items-center gap-4 mb-8">
                <div className="p-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full shadow-lg">
                  <TrendingUp className="h-8 w-8 text-white" />
                </div>
                <h2 className="section-header">Flight Recommendations</h2>
              </div>
              {recommendations.outbound.length > 0 && (
                <div className="mb-8">
                  <h3 className="font-bold text-lg mb-2 text-blue-700">Top Outbound Options</h3>
                  <div className="space-y-8">
                    {recommendations.outbound.map((rec, index) => (
                      <div
                        key={index}
                        className={`flight-option hover-lift card-shadow ${
                          rec.type === 'SYN FLIGHT' ? 'synthetic-route' :
                          rec.type === 'RT FLIGHT' ? 'roundtrip-route' :
                          rec.type === 'DIR FLIGHT' ? 'direct-route' : ''
                        }`}
                      >
                        <div className="flex items-start justify-between mb-6">
                          <div className="flex items-center gap-4">
                            {getRouteTypeBadge(rec.type)}
                            <span className="font-bold text-gray-800 text-lg">{rec.airline}</span>
                          </div>
                          <div className="text-right">
                            <div className="price-display">{formatPrice(rec.price)}</div>
                            <div className="text-sm text-gray-600 font-medium">
                              {rec.distance} mi • {formatVPM(rec.vpm)}
                            </div>
                          </div>
                        </div>

                        {rec.legs && rec.legs.length > 0 && (
                          <div className="space-y-4">
                            {rec.legs.map((leg, legIndex) => (
                              <div key={legIndex} className="leg-item">
                                <div className="flex-1">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="font-bold text-gray-800">{leg.airline}</span>
                                    <span className="text-green-600 font-bold text-lg">
                                      {formatPrice(leg.price)}
                                    </span>
                                  </div>
                                  <div className="text-gray-600 text-sm font-medium">
                                    {leg.origin} → {leg.destination}
                                  </div>
                                  <div className="text-gray-500 text-xs">
                                    {leg.departure} → {leg.arrival}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                        {!rec.legs && (
                          <div className="flex items-center justify-between text-sm text-gray-600 font-medium">
                            <span>Direct flight</span>
                            <span>Distance: {rec.distance} miles</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recommendations.misc.length > 0 && (
                <div className="mb-8">
                  <h3 className="font-bold text-lg mb-2 text-green-700">Other Redemption Options</h3>
                  <div className="space-y-8">
                    {recommendations.misc.map((rec, index) => (
                      <div
                        key={index}
                        className={`flight-option hover-lift card-shadow ${
                          rec.type === 'SYN FLIGHT' ? 'synthetic-route' :
                          rec.type === 'RT FLIGHT' ? 'roundtrip-route' :
                          rec.type === 'DIR FLIGHT' ? 'direct-route' : ''
                        }`}
                      >
                        <div className="flex items-start justify-between mb-6">
                          <div className="flex items-center gap-4">
                            {getRouteTypeBadge(rec.type)}
                            <span className="font-bold text-gray-800 text-lg">{rec.airline}</span>
                          </div>
                          <div className="text-right">
                            <div className="price-display">{formatPrice(rec.price)}</div>
                            <div className="text-sm text-gray-600 font-medium">
                              {rec.distance} mi • {formatVPM(rec.vpm)}
                            </div>
                          </div>
                        </div>

                        {rec.legs && rec.legs.length > 0 && (
                          <div className="space-y-4">
                            {rec.legs.map((leg, legIndex) => (
                              <div key={legIndex} className="leg-item">
                                <div className="flex-1">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="font-bold text-gray-800">{leg.airline}</span>
                                    <span className="text-green-600 font-bold text-lg">
                                      {formatPrice(leg.price)}
                                    </span>
                                  </div>
                                  <div className="text-gray-600 text-sm font-medium">
                                    {leg.origin} → {leg.destination}
                                  </div>
                                  <div className="text-gray-500 text-xs">
                                    {leg.departure} → {leg.arrival}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}

                        {!rec.legs && (
                          <div className="flex items-center justify-between text-sm text-gray-600 font-medium">
                            <span>Direct flight</span>
                            <span>Distance: {rec.distance} miles</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}

          {/* Empty State */}
          {!loading && (recommendations.outbound.length === 0 && recommendations.misc.length === 0) && !error && (
            <div className="empty-state">
              <div className="empty-state-icon">
                <Plane className="h-16 w-16 text-white/80" />
              </div>
              <h3 className="text-2xl font-black text-white mb-4 drop-shadow-lg">Ready to Find Your Perfect Flight?</h3>
              <p className="text-white/90 text-lg font-medium">Enter your travel details above to discover the best value options.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
