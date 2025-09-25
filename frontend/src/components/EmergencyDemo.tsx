import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MapPin, Mail, Clock, AlertTriangle } from 'lucide-react';
import { sendEmergencyAlert, LocationData } from '@/services/emailService';

const EmergencyDemo = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [lastLocation, setLastLocation] = useState<LocationData | null>(null);
  const [lastResult, setLastResult] = useState<{ success: boolean; error?: string } | null>(null);

  const handleTestEmergency = async () => {
    setIsLoading(true);
    setLastResult(null);
    
    try {
      const result = await sendEmergencyAlert('Demo Test', 'This is a demonstration of the emergency alert system.');
      setLastResult(result);
      if (result.success && result.locationData) {
        setLastLocation(result.locationData);
      }
    } catch (error) {
      setLastResult({ 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-emergency" />
          Emergency SOS Demo
        </CardTitle>
        <CardDescription>
          Test the emergency alert system with location tracking and email notifications
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button 
          onClick={handleTestEmergency}
          disabled={isLoading}
          className="w-full bg-emergency hover:bg-emergency/90"
        >
          {isLoading ? 'Testing Emergency Alert...' : 'Test Emergency Alert'}
        </Button>

        {lastResult && (
          <div className="space-y-3">
            <Badge variant={lastResult.success ? "default" : "destructive"}>
              {lastResult.success ? '✅ Alert Sent Successfully' : '❌ Alert Failed'}
            </Badge>
            
            {lastResult.error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-800">Error: {lastResult.error}</p>
              </div>
            )}

            {lastLocation && (
              <div className="space-y-2">
                <h4 className="font-medium flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  Location Captured
                </h4>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="font-medium">Latitude:</span> {lastLocation.latitude.toFixed(6)}
                  </div>
                  <div>
                    <span className="font-medium">Longitude:</span> {lastLocation.longitude.toFixed(6)}
                  </div>
                  <div>
                    <span className="font-medium">Accuracy:</span> {lastLocation.accuracy}m
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    <span className="font-medium">Time:</span> {new Date(lastLocation.timestamp).toLocaleTimeString()}
                  </div>
                </div>
                
                <div className="pt-2">
                  <a 
                    href={lastLocation.mapLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 text-sm"
                  >
                    <MapPin className="h-4 w-4" />
                    Open in Google Maps
                  </a>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="text-xs text-gray-500 space-y-1">
          <p>• This demo will request your location permission</p>
          <p>• A test email will be sent to the configured emergency contact</p>
          <p>• Check your browser console for detailed logs</p>
          <p>• Make sure EmailJS is properly configured in your .env file</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default EmergencyDemo;
