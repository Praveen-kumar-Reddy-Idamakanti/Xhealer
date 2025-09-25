# EmailJS Setup Guide for Emergency SOS Feature

This guide will help you set up EmailJS to enable the emergency SOS feature that sends location data via email.

## Prerequisites

1. An EmailJS account (free at [emailjs.com](https://www.emailjs.com/))
2. A Gmail account or other email service for sending emails

## Step 1: Create EmailJS Account

1. Go to [emailjs.com](https://www.emailjs.com/) and sign up for a free account
2. Verify your email address

## Step 2: Add Email Service

1. In your EmailJS dashboard, go to "Email Services"
2. Click "Add New Service"
3. Choose your email provider (Gmail recommended)
4. Follow the setup instructions for your chosen provider
5. Note down the **Service ID** (e.g., `service_xxxxxxx`)

## Step 3: Create Email Template

1. Go to "Email Templates" in your EmailJS dashboard
2. Click "Create New Template"
3. Use this template content:

### Template Subject:
```
Emergency SOS Alert - {{emergency_type}}
```

### Template Body:
```
Emergency Alert Details:

Type: {{emergency_type}}
Time: {{timestamp}}
From: {{from_name}}

Location Information:
{{location_data}}

Google Maps Link: {{map_link}}

Message:
{{message}}

---
This is an automated emergency alert. Please respond immediately.
```

4. Save the template and note down the **Template ID** (e.g., `template_xxxxxxx`)

## Step 4: Get Public Key

1. Go to "Account" in your EmailJS dashboard
2. Find your **Public Key** (e.g., `xxxxxxxxxxxxxxxx`)

## Step 5: Configure Environment Variables

1. Copy the `env.example` file to `.env` in the frontend directory:
   ```bash
   cp env.example .env
   ```

2. Edit the `.env` file with your actual values:
   ```env
   # EmailJS Configuration
   VITE_EMAILJS_SERVICE_ID=service_xxxxxxx
   VITE_EMAILJS_TEMPLATE_ID=template_xxxxxxx
   VITE_EMAILJS_PUBLIC_KEY=xxxxxxxxxxxxxxxx

   # Emergency Contact Email
   VITE_EMERGENCY_CONTACT_EMAIL=emergency@yourdomain.com
   ```

## Step 6: Test the Setup

1. Start your development server:
   ```bash
   npm run dev
   ```

2. Click the SOS button in your application
3. Check if the emergency email is sent successfully

## Template Variables

The email template uses these variables:
- `{{to_email}}` - Recipient email address
- `{{from_name}}` - Sender name (Emergency Alert System)
- `{{emergency_type}}` - Type of emergency (Emergency SOS)
- `{{location_data}}` - GPS coordinates and accuracy
- `{{map_link}}` - Google Maps link to the location
- `{{timestamp}}` - When the emergency was triggered
- `{{message}}` - Additional emergency message

## Troubleshooting

### Common Issues:

1. **"EmailJS public key not found"**
   - Make sure your `.env` file is in the frontend directory
   - Ensure the variable names start with `VITE_`
   - Restart your development server after adding environment variables

2. **"EmailJS configuration is incomplete"**
   - Verify all three EmailJS IDs are correctly set in your `.env` file
   - Check that the Service ID and Template ID exist in your EmailJS dashboard

3. **"Failed to send email"**
   - Check your email service configuration in EmailJS
   - Verify the template variables match the template you created
   - Check the browser console for detailed error messages

4. **Location permission denied**
   - Make sure the user grants location permission when prompted
   - The app must be served over HTTPS for geolocation to work in production

### Testing Location Feature:

1. Open browser developer tools (F12)
2. Go to the Console tab
3. Click the SOS button and watch for location-related messages
4. Check if the location coordinates are being captured correctly

## Security Notes

- Never commit your `.env` file to version control
- The EmailJS public key is safe to expose in frontend code
- Consider rate limiting for the SOS feature to prevent abuse
- Monitor your EmailJS usage to stay within free tier limits

## Production Deployment

1. Set the environment variables in your hosting platform
2. Ensure your domain is added to EmailJS allowed origins
3. Test the feature thoroughly before going live
4. Consider implementing additional security measures

## Support

If you encounter issues:
1. Check the EmailJS documentation: [docs.emailjs.com](https://docs.emailjs.com/)
2. Verify your email service configuration
3. Test with a simple email template first
4. Check browser console for detailed error messages
