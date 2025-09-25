import emailjs from '@emailjs/browser';

// EmailJS configuration
const EMAILJS_SERVICE_ID = import.meta.env.VITE_EMAILJS_SERVICE_ID;
const EMAILJS_TEMPLATE_ID = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
const EMAILJS_PUBLIC_KEY = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;
const EMERGENCY_CONTACT_EMAIL = import.meta.env.VITE_EMERGENCY_CONTACT_EMAIL;

export interface LocationData {
  latitude: number;
  longitude: number;
  accuracy?: number;
  timestamp: string;
  mapLink: string;
}

export interface EmergencyEmailData {
  to_email: string;
  from_name: string;
  emergency_type: string;
  location_data: string;
  map_link: string;
  timestamp: string;
  message: string;
}

// Initialize EmailJS
export const initializeEmailJS = () => {
  if (!EMAILJS_PUBLIC_KEY) {
    console.error('EmailJS public key not found in environment variables');
    return false;
  }
  
  emailjs.init(EMAILJS_PUBLIC_KEY);
  return true;
};

// Get user's current location
export const getCurrentLocation = (): Promise<LocationData> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser'));
      return;
    }

    const options: PositionOptions = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    };

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude, accuracy } = position.coords;
        const timestamp = new Date().toISOString();
        const mapLink = `https://www.google.com/maps?q=${latitude},${longitude}`;
        
        resolve({
          latitude,
          longitude,
          accuracy,
          timestamp,
          mapLink
        });
      },
      (error) => {
        console.error('Error getting location:', error);
        reject(error);
      },
      options
    );
  });
};

// Send emergency email with location data
export const sendEmergencyEmail = async (
  locationData: LocationData,
  emergencyType: string = 'Emergency SOS',
  additionalMessage: string = ''
): Promise<boolean> => {
  try {
    if (!EMAILJS_SERVICE_ID || !EMAILJS_TEMPLATE_ID) {
      throw new Error('EmailJS configuration is incomplete');
    }

    const emailData: EmergencyEmailData = {
      to_email: EMERGENCY_CONTACT_EMAIL || 'emergency@example.com',
      from_name: 'Emergency Alert System',
      emergency_type: emergencyType,
      location_data: `Latitude: ${locationData.latitude}, Longitude: ${locationData.longitude}, Accuracy: ${locationData.accuracy}m`,
      map_link: locationData.mapLink,
      timestamp: locationData.timestamp,
      message: additionalMessage || 'Emergency SOS activated. Please check the location and provide immediate assistance.'
    };

    const response = await emailjs.send(
      EMAILJS_SERVICE_ID,
      EMAILJS_TEMPLATE_ID,
      emailData
    );

    console.log('Emergency email sent successfully:', response);
    return true;
  } catch (error) {
    console.error('Error sending emergency email:', error);
    return false;
  }
};

// Send emergency alert with location
export const sendEmergencyAlert = async (
  emergencyType: string = 'Emergency SOS',
  additionalMessage: string = ''
): Promise<{ success: boolean; locationData?: LocationData; error?: string }> => {
  try {
    // Get current location
    const locationData = await getCurrentLocation();
    
    // Send email
    const emailSent = await sendEmergencyEmail(locationData, emergencyType, additionalMessage);
    
    if (emailSent) {
      return { success: true, locationData };
    } else {
      return { success: false, error: 'Failed to send email' };
    }
  } catch (error) {
    console.error('Emergency alert failed:', error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error occurred' 
    };
  }
};
