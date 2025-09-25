import { sendEmergencyAlert, initializeEmailJS } from '@/services/emailService';

/**
 * Test utility to verify EmailJS configuration
 * This can be called from browser console for testing
 */
export const testEmailJS = async () => {
  console.log('Testing EmailJS configuration...');
  
  // Check environment variables
  const serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID;
  const templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
  const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;
  const emergencyEmail = import.meta.env.VITE_EMERGENCY_CONTACT_EMAIL;
  
  console.log('Environment variables:');
  console.log('- Service ID:', serviceId ? '✓ Set' : '✗ Missing');
  console.log('- Template ID:', templateId ? '✓ Set' : '✗ Missing');
  console.log('- Public Key:', publicKey ? '✓ Set' : '✗ Missing');
  console.log('- Emergency Email:', emergencyEmail ? '✓ Set' : '✗ Missing');
  
  if (!serviceId || !templateId || !publicKey) {
    console.error('❌ EmailJS configuration incomplete. Please check your .env file.');
    return false;
  }
  
  // Initialize EmailJS
  const initialized = initializeEmailJS();
  if (!initialized) {
    console.error('❌ Failed to initialize EmailJS');
    return false;
  }
  
  console.log('✓ EmailJS initialized successfully');
  
  // Test emergency alert (this will request location permission)
  try {
    console.log('Testing emergency alert...');
    const result = await sendEmergencyAlert('Test Alert', 'This is a test emergency alert to verify EmailJS setup.');
    
    if (result.success) {
      console.log('✅ Test email sent successfully!');
      console.log('Location data:', result.locationData);
      return true;
    } else {
      console.error('❌ Test email failed:', result.error);
      return false;
    }
  } catch (error) {
    console.error('❌ Test failed with error:', error);
    return false;
  }
};

// Make it available globally for console testing
if (typeof window !== 'undefined') {
  (window as any).testEmailJS = testEmailJS;
}
