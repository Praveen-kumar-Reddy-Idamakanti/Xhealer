-- HealthCare AI Database Schema
-- This SQL script creates all necessary tables for the HealthCare AI application

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE user_type AS ENUM ('authenticated', 'guest');
CREATE TYPE consultation_status AS ENUM ('scheduled', 'completed', 'cancelled', 'rescheduled');
CREATE TYPE emergency_contact_relationship AS ENUM ('spouse', 'parent', 'child', 'sibling', 'friend', 'other');

-- 1. User Profiles Table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    user_type user_type NOT NULL DEFAULT 'authenticated',
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(20),
    language VARCHAR(10) DEFAULT 'en',
    profile_picture_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Emergency Contacts Table
CREATE TABLE emergency_contacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    relationship emergency_contact_relationship NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Doctor Consultations Table
CREATE TABLE consultations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    doctor_name VARCHAR(255) NOT NULL,
    doctor_specialty VARCHAR(100) NOT NULL,
    doctor_phone VARCHAR(20),
    doctor_email VARCHAR(255),
    consultation_date DATE NOT NULL,
    consultation_time TIME NOT NULL,
    status consultation_status DEFAULT 'scheduled',
    notes TEXT,
    prescription_url TEXT,
    follow_up_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Symptom Analysis History Table
CREATE TABLE symptom_analysis_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    symptoms TEXT[] NOT NULL,
    predicted_disease VARCHAR(255) NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL,
    top_predictions JSONB,
    analysis_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    follow_up_required BOOLEAN DEFAULT false,
    follow_up_notes TEXT
);

-- 5. Medical Reports Table
CREATE TABLE medical_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(100) NOT NULL,
    file_url TEXT NOT NULL,
    file_size INTEGER,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    report_date DATE,
    doctor_name VARCHAR(255),
    notes TEXT
);

-- 6. Health Reminders Table
CREATE TABLE health_reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    reminder_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    reminder_date DATE NOT NULL,
    reminder_time TIME,
    is_completed BOOLEAN DEFAULT false,
    is_recurring BOOLEAN DEFAULT false,
    recurrence_pattern VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. User Preferences Table
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en',
    notifications_enabled BOOLEAN DEFAULT true,
    email_notifications BOOLEAN DEFAULT true,
    sms_notifications BOOLEAN DEFAULT false,
    emergency_alerts BOOLEAN DEFAULT true,
    data_sharing_consent BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_email ON user_profiles(email);
CREATE INDEX idx_emergency_contacts_user_id ON emergency_contacts(user_id);
CREATE INDEX idx_consultations_user_id ON consultations(user_id);
CREATE INDEX idx_consultations_date ON consultations(consultation_date);
CREATE INDEX idx_symptom_analysis_user_id ON symptom_analysis_history(user_id);
CREATE INDEX idx_symptom_analysis_timestamp ON symptom_analysis_history(analysis_timestamp);
CREATE INDEX idx_medical_reports_user_id ON medical_reports(user_id);
CREATE INDEX idx_health_reminders_user_id ON health_reminders(user_id);
CREATE INDEX idx_health_reminders_date ON health_reminders(reminder_date);
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_emergency_contacts_updated_at BEFORE UPDATE ON emergency_contacts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_consultations_updated_at BEFORE UPDATE ON consultations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) Policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE emergency_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultations ENABLE ROW LEVEL SECURITY;
ALTER TABLE symptom_analysis_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own profile" ON user_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own profile" ON user_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);

-- RLS Policies for emergency_contacts
CREATE POLICY "Users can view own emergency contacts" ON emergency_contacts FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can manage own emergency contacts" ON emergency_contacts FOR ALL USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- RLS Policies for consultations
CREATE POLICY "Users can view own consultations" ON consultations FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can manage own consultations" ON consultations FOR ALL USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- RLS Policies for symptom_analysis_history
CREATE POLICY "Users can view own symptom analysis" ON symptom_analysis_history FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can insert own symptom analysis" ON symptom_analysis_history FOR INSERT WITH CHECK (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- RLS Policies for medical_reports
CREATE POLICY "Users can view own medical reports" ON medical_reports FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can manage own medical reports" ON medical_reports FOR ALL USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- RLS Policies for health_reminders
CREATE POLICY "Users can view own health reminders" ON health_reminders FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can manage own health reminders" ON health_reminders FOR ALL USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- RLS Policies for user_preferences
CREATE POLICY "Users can view own preferences" ON user_preferences FOR SELECT USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);
CREATE POLICY "Users can manage own preferences" ON user_preferences FOR ALL USING (
    user_id IN (SELECT id FROM user_profiles WHERE user_id = auth.uid())
);

-- Sample data will be created automatically when users sign up through the application
-- The handle_new_user() trigger function will create user profiles and preferences automatically

-- Create a function to handle user profile creation on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_profiles (user_id, email, full_name, user_type)
    VALUES (NEW.id, NEW.email, COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email), 'authenticated');
    
    INSERT INTO user_preferences (user_id)
    VALUES (NEW.id);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Create a function to get user profile with all related data
CREATE OR REPLACE FUNCTION get_user_profile_complete(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'profile', row_to_json(up),
        'emergency_contacts', (
            SELECT json_agg(row_to_json(ec))
            FROM emergency_contacts ec
            WHERE ec.user_id = up.id
        ),
        'consultations', (
            SELECT json_agg(row_to_json(c))
            FROM consultations c
            WHERE c.user_id = up.id
            ORDER BY c.consultation_date DESC
        ),
        'symptom_history', (
            SELECT json_agg(row_to_json(sah))
            FROM symptom_analysis_history sah
            WHERE sah.user_id = up.id
            ORDER BY sah.analysis_timestamp DESC
            LIMIT 10
        ),
        'health_reminders', (
            SELECT json_agg(row_to_json(hr))
            FROM health_reminders hr
            WHERE hr.user_id = up.id
            AND hr.reminder_date >= CURRENT_DATE
            ORDER BY hr.reminder_date ASC
        ),
        'preferences', (
            SELECT row_to_json(upref)
            FROM user_preferences upref
            WHERE upref.user_id = up.id
        )
    ) INTO result
    FROM user_profiles up
    WHERE up.user_id = user_uuid;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

-- Create a view for easy access to user data
CREATE VIEW user_dashboard_data AS
SELECT 
    up.id,
    up.user_id,
    up.email,
    up.full_name,
    up.phone,
    up.user_type,
    up.created_at,
    COUNT(DISTINCT ec.id) as emergency_contacts_count,
    COUNT(DISTINCT c.id) as consultations_count,
    COUNT(DISTINCT sah.id) as symptom_analyses_count,
    COUNT(DISTINCT hr.id) as active_reminders_count
FROM user_profiles up
LEFT JOIN emergency_contacts ec ON up.id = ec.user_id
LEFT JOIN consultations c ON up.id = c.user_id
LEFT JOIN symptom_analysis_history sah ON up.id = sah.user_id
LEFT JOIN health_reminders hr ON up.id = hr.user_id AND hr.reminder_date >= CURRENT_DATE
GROUP BY up.id, up.user_id, up.email, up.full_name, up.phone, up.user_type, up.created_at;

-- Grant access to the view
GRANT SELECT ON user_dashboard_data TO authenticated;
