import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertTriangle, Phone, MapPin, Mail, Loader2 } from 'lucide-react';
import { sendEmergencyAlert, initializeEmailJS, LocationData } from '@/services/emailService';

const SOSButton = () => {
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [isCountdownActive, setIsCountdownActive] = useState(false);
  const [countdown, setCountdown] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const [locationData, setLocationData] = useState<LocationData | null>(null);
  const [emailSent, setEmailSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize EmailJS on component mount
  useEffect(() => {
    initializeEmailJS();
  }, []);

  const handleSOSClick = () => {
    setIsConfirmOpen(true);
  };

  const handleConfirm = () => {
    setIsConfirmOpen(false);
    setIsCountdownActive(true);
    
    // Start countdown
    let count = 10;
    const timer = setInterval(() => {
      count--;
      setCountdown(count);
      
      if (count <= 0) {
        clearInterval(timer);
        triggerEmergency();
        setIsCountdownActive(false);
        setCountdown(10);
      }
    }, 1000);

    // Store timer ID to clear if cancelled
    (window as any).sosTimer = timer;
  };

  const handleCancel = () => {
    if ((window as any).sosTimer) {
      clearInterval((window as any).sosTimer);
    }
    setIsConfirmOpen(false);
    setIsCountdownActive(false);
    setCountdown(10);
  };

  const triggerEmergency = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Send emergency alert with location
      const result = await sendEmergencyAlert('Emergency SOS', 'User has activated emergency SOS button. Please provide immediate assistance.');
      
      if (result.success) {
        setLocationData(result.locationData || null);
        setEmailSent(true);
        
        // Show success message with location details
        const locationInfo = result.locationData 
          ? `\nLocation: ${result.locationData.latitude}, ${result.locationData.longitude}\nMap: ${result.locationData.mapLink}`
          : '';
        
        alert(`Emergency services have been contacted. Help is on the way!${locationInfo}`);
      } else {
        setError(result.error || 'Failed to send emergency alert');
        alert(`Emergency alert failed: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(errorMessage);
      alert(`Emergency alert failed: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  if (isCountdownActive) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <div className="bg-emergency text-white rounded-full p-6 shadow-emergency animate-pulse">
          <div className="text-center">
            <div className="text-2xl font-bold">{countdown}</div>
            <div className="text-xs">Calling emergency</div>
            {isLoading && (
              <div className="flex items-center justify-center mt-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-xs ml-1">Getting location...</span>
              </div>
            )}
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          className="mt-2 w-full bg-white"
          onClick={handleCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
      </div>
    );
  }

  return (
    <>
      <Button
        className="fixed bottom-6 right-6 z-50 h-16 w-16 rounded-full bg-emergency hover:bg-emergency/90 shadow-emergency"
        onClick={handleSOSClick}
      >
        <div className="text-center">
          <AlertTriangle className="h-6 w-6 mb-1" />
          <div className="text-xs font-bold">SOS</div>
        </div>
      </Button>

      <Dialog open={isConfirmOpen} onOpenChange={setIsConfirmOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-emergency">
              <AlertTriangle className="h-5 w-5" />
              Emergency Alert
            </DialogTitle>
            <DialogDescription>
              Are you sure you want to trigger emergency services? This will:
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              <span>Call emergency services (108)</span>
            </div>
            <div className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              <span>Send email alert to emergency contacts</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4" />
              <span>Share your current location with GPS coordinates</span>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span>Include Google Maps link for easy navigation</span>
            </div>
          </div>

          <DialogFooter className="gap-2">
            <Button variant="outline" onClick={handleCancel}>
              Cancel
            </Button>
            <Button 
              className="bg-emergency hover:bg-emergency/90"
              onClick={handleConfirm}
            >
              Confirm Emergency
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default SOSButton;