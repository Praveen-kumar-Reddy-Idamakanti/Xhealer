import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertTriangle, Phone } from 'lucide-react';

const SOSButton = () => {
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [isCountdownActive, setIsCountdownActive] = useState(false);
  const [countdown, setCountdown] = useState(10);

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

  const triggerEmergency = () => {
    // Mock emergency actions
    console.log('Emergency triggered');
    // Here would be:
    // 1. Call emergency number
    // 2. Send notifications to emergency contacts
    // 3. Log emergency event in Firestore
    // 4. Send location data
    
    alert('Emergency services have been contacted. Help is on the way.');
  };

  if (isCountdownActive) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <div className="bg-emergency text-white rounded-full p-6 shadow-emergency animate-pulse">
          <div className="text-center">
            <div className="text-2xl font-bold">{countdown}</div>
            <div className="text-xs">Calling emergency</div>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          className="mt-2 w-full bg-white"
          onClick={handleCancel}
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
              <AlertTriangle className="h-4 w-4" />
              <span>Notify your emergency contacts</span>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              <span>Share your current location</span>
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