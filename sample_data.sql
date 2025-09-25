-- Sample Data Script for HealthCare AI Application
-- Run this script AFTER you have created actual users in Supabase Auth
-- Replace the UUIDs below with actual user IDs from your auth.users table

-- First, check what users exist in your auth.users table:
-- SELECT id, email FROM auth.users;

-- Then replace the UUIDs below with actual user IDs and run this script

-- Insert sample emergency contacts (replace UUIDs with actual user profile IDs)
-- INSERT INTO emergency_contacts (user_id, name, relationship, phone, email, is_primary) VALUES
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'John Johnson', 'spouse', '+91-9876543211', 'john.johnson@email.com', true),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'Mary Johnson', 'parent', '+91-9876543212', 'mary.johnson@email.com', false),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_2'), 'Jane Doe', 'spouse', '+91-9876543213', 'jane.doe@email.com', true);

-- Insert sample consultations
-- INSERT INTO consultations (user_id, doctor_name, doctor_specialty, doctor_phone, consultation_date, consultation_time, status, notes) VALUES
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'Dr. Priya Sharma', 'Cardiologist', '+91-9876543220', '2024-01-15', '14:30:00', 'scheduled', 'Regular checkup for heart condition'),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'Dr. Rajesh Kumar', 'General Physician', '+91-9876543221', '2023-12-20', '11:00:00', 'completed', 'Annual health checkup completed'),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_2'), 'Dr. Anjali Patel', 'Dermatologist', '+91-9876543222', '2024-01-20', '10:00:00', 'scheduled', 'Skin condition consultation');

-- Insert sample symptom analysis history
-- INSERT INTO symptom_analysis_history (user_id, symptoms, predicted_disease, confidence_score, top_predictions, follow_up_required) VALUES
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 
--  ARRAY['headache', 'fever', 'fatigue'], 
--  'Common Cold', 
--  85.5, 
--  '{"predictions": [{"disease": "Common Cold", "confidence": 85.5}, {"disease": "Flu", "confidence": 12.3}]}',
--  false),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 
--  ARRAY['chest pain', 'shortness of breath'], 
--  'Anxiety', 
--  78.2, 
--  '{"predictions": [{"disease": "Anxiety", "confidence": 78.2}, {"disease": "Stress", "confidence": 15.8}]}',
--  true),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_2'), 
--  ARRAY['skin rash', 'itching'], 
--  'Allergic Reaction', 
--  92.1, 
--  '{"predictions": [{"disease": "Allergic Reaction", "confidence": 92.1}, {"disease": "Eczema", "confidence": 5.2}]}',
--  false);

-- Insert sample health reminders
-- INSERT INTO health_reminders (user_id, reminder_type, title, description, reminder_date, reminder_time, is_recurring, recurrence_pattern) VALUES
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'medication', 'Take Blood Pressure Medicine', 'Take prescribed blood pressure medication', '2024-01-15', '08:00:00', true, 'daily'),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_1'), 'appointment', 'Annual Checkup', 'Schedule annual health checkup', '2024-02-01', '09:00:00', true, 'yearly'),
-- ((SELECT id FROM user_profiles WHERE user_id = 'REPLACE_WITH_ACTUAL_USER_ID_2'), 'exercise', 'Morning Walk', '30-minute morning walk', '2024-01-16', '07:00:00', true, 'daily');

-- Instructions:
-- 1. First, create users in your Supabase Auth dashboard or through your application
-- 2. Run this query to get the actual user IDs: SELECT id, email FROM auth.users;
-- 3. Replace 'REPLACE_WITH_ACTUAL_USER_ID_1' and 'REPLACE_WITH_ACTUAL_USER_ID_2' with actual UUIDs
-- 4. Uncomment the INSERT statements above and run them
