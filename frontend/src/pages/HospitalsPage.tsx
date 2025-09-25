import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { ArrowLeft, MapPin, Phone, Navigation, Clock, Search, RefreshCw, Copy, Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Hospital {
  id: string;
  name: string;
  address: string;
  phone: string;
  distance: number;
  type: string[];
  rating: number;
  openNow: boolean;
  emergencyServices: boolean;
}

const HospitalsPage = () => {
  const navigate = useNavigate();
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [locationAccuracy, setLocationAccuracy] = useState<number | null>(null);
  const [locationTimestamp, setLocationTimestamp] = useState<Date | null>(null);
  const [isRefreshingLocation, setIsRefreshingLocation] = useState(false);
  const [copiedToClipboard, setCopiedToClipboard] = useState(false);

  const mockHospitals: Hospital[] = [
    {
      id: '1',
      name: 'Apollo Hospital',
      address: '123 Medical District, Downtown',
      phone: '+91-9876543210',
      distance: 1.2,
      type: ['General', 'Emergency', 'Cardiology'],
      rating: 4.5,
      openNow: true,
      emergencyServices: true
    },
    {
      id: '2',
      name: 'Max Healthcare',
      address: '456 Health Avenue, Central',
      phone: '+91-9876543211',
      distance: 2.1,
      type: ['General', 'Pediatrics', 'Neurology'],
      rating: 4.3,
      openNow: true,
      emergencyServices: true
    },
    {
      id: '3',
      name: 'City Medical Center',
      address: '789 Care Street, North Zone',
      phone: '+91-9876543212',
      distance: 3.5,
      type: ['General', 'Orthopedics'],
      rating: 4.1,
      openNow: false,
      emergencyServices: false
    },
    {
      id: '4',
      name: 'Emergency Care Hospital',
      address: '321 Urgent Care Blvd',
      phone: '+91-9876543213',
      distance: 4.2,
      type: ['Emergency', 'Trauma'],
      rating: 4.7,
      openNow: true,
      emergencyServices: true
    }
  ];

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      setIsRefreshingLocation(true);
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          setLocationAccuracy(position.coords.accuracy);
          setLocationTimestamp(new Date());
          setIsRefreshingLocation(false);
        },
        (error) => {
          console.error('Error getting location:', error);
          setIsRefreshingLocation(false);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutes
        }
      );
    }
  };

  useEffect(() => {
    // Get user location on component mount
    getCurrentLocation();

    // Load hospitals (sorted by distance)
    const sortedHospitals = mockHospitals.sort((a, b) => a.distance - b.distance);
    setHospitals(sortedHospitals);
  }, []);

  const filteredHospitals = hospitals.filter(hospital =>
    hospital.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    hospital.type.some(t => t.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleCall = (phone: string) => {
    window.open(`tel:${phone}`, '_self');
  };

  const handleNavigate = (address: string) => {
    const encodedAddress = encodeURIComponent(address);
    window.open(`https://www.google.com/maps/search/${encodedAddress}`, '_blank');
  };

  const copyCoordinates = async () => {
    if (userLocation) {
      const coordinates = `${userLocation.lat}, ${userLocation.lng}`;
      try {
        await navigator.clipboard.writeText(coordinates);
        setCopiedToClipboard(true);
        setTimeout(() => setCopiedToClipboard(false), 2000);
      } catch (err) {
        console.error('Failed to copy coordinates:', err);
      }
    }
  };

  const openInMaps = () => {
    if (userLocation) {
      const url = `https://www.google.com/maps?q=${userLocation.lat},${userLocation.lng}`;
      window.open(url, '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-background">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-xl font-semibold">Nearby Hospitals</h1>
            <p className="text-sm text-muted-foreground">
              {userLocation ? 'Showing hospitals near your location' : 'Location access needed for accurate results'}
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4 space-y-4">
        {/* Search Bar */}
        <Card className="shadow-card-custom">
          <CardContent className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search hospitals or specialties..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Live Location Display */}
        {userLocation ? (
          <Card className="shadow-card-custom border-accent">
            <CardContent className="p-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-accent">
                    <MapPin className="h-4 w-4" />
                    <span className="text-sm font-medium">Live Location Detected</span>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={getCurrentLocation}
                    disabled={isRefreshingLocation}
                    className="h-8"
                  >
                    <RefreshCw className={`h-3 w-3 mr-1 ${isRefreshingLocation ? 'animate-spin' : ''}`} />
                    Refresh
                  </Button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Coordinates */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium text-muted-foreground">Coordinates</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={copyCoordinates}
                        className="h-6 px-2"
                      >
                        {copiedToClipboard ? (
                          <Check className="h-3 w-3 text-green-600" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                      </Button>
                    </div>
                    <div className="bg-muted/50 rounded-md p-2 font-mono text-sm">
                      <div>Lat: {userLocation.lat.toFixed(6)}</div>
                      <div>Lng: {userLocation.lng.toFixed(6)}</div>
                    </div>
                  </div>
                  
                  {/* Location Details */}
                  <div className="space-y-2">
                    <span className="text-xs font-medium text-muted-foreground">Location Details</span>
                    <div className="space-y-1 text-sm">
                      {locationAccuracy && (
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Accuracy:</span>
                          <span>{locationAccuracy.toFixed(0)}m</span>
                        </div>
                      )}
                      {locationTimestamp && (
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Updated:</span>
                          <span>{locationTimestamp.toLocaleTimeString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                {/* Action Buttons */}
                <div className="flex gap-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={openInMaps}
                    className="flex-1"
                  >
                    <Navigation className="h-3 w-3 mr-1" />
                    View in Maps
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={copyCoordinates}
                    className="flex-1"
                  >
                    {copiedToClipboard ? (
                      <>
                        <Check className="h-3 w-3 mr-1 text-green-600" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="h-3 w-3 mr-1" />
                        Copy Coords
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ) : (
          <Card className="shadow-card-custom border-orange-200">
            <CardContent className="p-4">
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-orange-600">
                  <MapPin className="h-4 w-4" />
                  <span className="text-sm font-medium">Location Access Required</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Enable location access to see hospitals near you and get accurate distance calculations.
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={getCurrentLocation}
                  disabled={isRefreshingLocation}
                  className="w-full"
                >
                  <RefreshCw className={`h-3 w-3 mr-1 ${isRefreshingLocation ? 'animate-spin' : ''}`} />
                  {isRefreshingLocation ? 'Detecting Location...' : 'Enable Location Access'}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Emergency Banner */}
        <Card className="shadow-card-custom border-emergency">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-emergency">
                <Phone className="h-5 w-5" />
                <span className="font-medium">Emergency? Call 108 for immediate assistance</span>
              </div>
              <Button 
                variant="outline" 
                className="border-emergency text-emergency hover:bg-emergency hover:text-white"
                onClick={() => handleCall('108')}
              >
                Call Now
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Hospitals List */}
        <div className="space-y-4">
          {filteredHospitals.map((hospital) => (
            <Card key={hospital.id} className="shadow-card-custom">
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-semibold">{hospital.name}</h3>
                      {hospital.emergencyServices && (
                        <Badge className="bg-emergency text-emergency-foreground">24/7 Emergency</Badge>
                      )}
                      {hospital.openNow ? (
                        <Badge className="bg-accent text-accent-foreground">Open Now</Badge>
                      ) : (
                        <Badge variant="outline">Closed</Badge>
                      )}
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <MapPin className="h-4 w-4" />
                        <span>{hospital.address}</span>
                      </div>
                      
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Navigation className="h-4 w-4" />
                        <span>{hospital.distance} km away</span>
                      </div>
                      
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Clock className="h-4 w-4" />
                        <span>Rating: {hospital.rating}/5.0</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Specialties */}
                <div className="mb-4">
                  <p className="text-sm font-medium mb-2">Specialties:</p>
                  <div className="flex flex-wrap gap-1">
                    {hospital.type.map((specialty, idx) => (
                      <Badge key={idx} variant="secondary">
                        {specialty}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <Button
                    variant="outline"
                    className="justify-center"
                    onClick={() => handleCall(hospital.phone)}
                  >
                    <Phone className="mr-2 h-4 w-4" />
                    Call Hospital
                  </Button>
                  
                  <Button
                    className="justify-center"
                    onClick={() => handleNavigate(hospital.address)}
                  >
                    <Navigation className="mr-2 h-4 w-4" />
                    Get Directions
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredHospitals.length === 0 && (
          <Card className="shadow-card-custom">
            <CardContent className="p-8 text-center">
              <MapPin className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">No hospitals found matching your search.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default HospitalsPage;