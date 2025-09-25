import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { 
  ArrowLeft, 
  User, 
  Phone, 
  Mail, 
  Calendar,
  FileText,
  Clock,
  Users,
  Settings,
  LogOut,
  Edit2,
  Upload,
  Plus,
  Trash2
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { supabase } from '@/integrations/supabase/client';
import { Database } from '@/integrations/supabase/types';
import { debugAuth } from '@/utils/debugAuth';

type EmergencyContact = Database['public']['Tables']['emergency_contacts']['Row'];
type Consultation = Database['public']['Tables']['consultations']['Row'];
type SymptomAnalysis = Database['public']['Tables']['symptom_analysis_history']['Row'];
type HealthReminder = Database['public']['Tables']['health_reminders']['Row'];

const Profile = () => {
  const navigate = useNavigate();
  const { user, profile, isGuest, userType, signOut, updateProfile, createProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [emergencyContacts, setEmergencyContacts] = useState<EmergencyContact[]>([]);
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [symptomHistory, setSymptomHistory] = useState<SymptomAnalysis[]>([]);
  const [healthReminders, setHealthReminders] = useState<HealthReminder[]>([]);
  const [profileData, setProfileData] = useState({
    full_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    language: 'en'
  });

  // Redirect if guest user
  useEffect(() => {
    if (isGuest) {
      console.log('Guest user detected, redirecting to dashboard');
      navigate('/dashboard');
    }
  }, [isGuest, navigate]);

  // Add timeout to prevent infinite loading
  useEffect(() => {
    const timer = setTimeout(() => {
      if (loading && !profile && !isGuest) {
        console.log('Profile loading timeout - redirecting to dashboard');
        navigate('/dashboard');
      }
    }, 10000); // 10 second timeout

    return () => clearTimeout(timer);
  }, [loading, profile, isGuest, navigate]);

  // Load profile data
  useEffect(() => {
    if (profile) {
      setProfileData({
        full_name: profile.full_name || '',
        email: profile.email || '',
        phone: profile.phone || '',
        date_of_birth: profile.date_of_birth || '',
        gender: profile.gender || '',
        language: profile.language || 'en'
      });
    }
  }, [profile]);

  // Load related data
  useEffect(() => {
    if (profile) {
      loadRelatedData();
    }
  }, [profile]);

  const loadRelatedData = async () => {
    if (!profile) return;

    try {
      // Load emergency contacts
      const { data: contacts } = await supabase
        .from('emergency_contacts')
        .select('*')
        .eq('user_id', profile.id)
        .order('is_primary', { ascending: false });

      // Load consultations
      const { data: consults } = await supabase
        .from('consultations')
        .select('*')
        .eq('user_id', profile.id)
        .order('consultation_date', { ascending: false });

      // Load symptom analysis history
      const { data: symptoms } = await supabase
        .from('symptom_analysis_history')
        .select('*')
        .eq('user_id', profile.id)
        .order('analysis_timestamp', { ascending: false })
        .limit(10);

      // Load health reminders
      const { data: reminders } = await supabase
        .from('health_reminders')
        .select('*')
        .eq('user_id', profile.id)
        .gte('reminder_date', new Date().toISOString().split('T')[0])
        .order('reminder_date', { ascending: true });

      setEmergencyContacts(contacts || []);
      setConsultations(consults || []);
      setSymptomHistory(symptoms || []);
      setHealthReminders(reminders || []);
    } catch (error) {
      console.error('Error loading related data:', error);
    }
  };

  const handleSaveProfile = async () => {
    if (!profile) return;
    
    setLoading(true);
    try {
      await updateProfile(profileData);
      setIsEditing(false);
    } catch (error) {
      console.error('Error saving profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await signOut();
    navigate('/');
  };

  const addEmergencyContact = async () => {
    if (!profile) return;
    
    const newContact: Database['public']['Tables']['emergency_contacts']['Insert'] = {
      user_id: profile.id,
      name: 'New Contact',
      relationship: 'other',
      phone: '',
      email: '',
      is_primary: false
    };

    try {
      const { data, error } = await supabase
        .from('emergency_contacts')
        .insert(newContact as any)
        .select()
        .single();

      if (error) throw error;
      setEmergencyContacts(prev => [...prev, data]);
    } catch (error) {
      console.error('Error adding emergency contact:', error);
    }
  };

  const deleteEmergencyContact = async (contactId: string) => {
    try {
      const { error } = await supabase
        .from('emergency_contacts')
        .delete()
        .eq('id', contactId);

      if (error) throw error;
      setEmergencyContacts(prev => prev.filter(contact => contact.id !== contactId));
    } catch (error) {
      console.error('Error deleting emergency contact:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'scheduled': return 'bg-primary text-primary-foreground';
      case 'completed': return 'bg-accent text-accent-foreground';
      case 'cancelled': return 'bg-destructive text-destructive-foreground';
      case 'rescheduled': return 'bg-orange-500 text-white';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  // Don't render if guest user
  if (isGuest) {
    return null;
  }

  // Debug logging
  console.log('Profile component state:', { user, profile, isGuest, loading, userType: userType });
  
  // Run debug auth on component mount
  useEffect(() => {
    debugAuth();
  }, []);

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading profile...</p>
          <p className="text-xs text-muted-foreground mt-2">
            User: {user ? 'Authenticated' : 'Not authenticated'} | 
            Guest: {isGuest ? 'Yes' : 'No'} | 
            Loading: {loading ? 'Yes' : 'No'}
          </p>
        </div>
      </div>
    );
  }

  // Show error state if no profile and not loading
  if (!profile && !loading && !isGuest) {
    return (
      <div className="min-h-screen bg-gradient-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Unable to load profile</p>
          <Button onClick={() => navigate('/dashboard')}>
            Return to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-background">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div className="flex-1">
            <h1 className="text-xl font-semibold">Profile</h1>
            <p className="text-sm text-muted-foreground">Manage your health information</p>
          </div>
          <Button variant="outline" onClick={() => setIsEditing(!isEditing)}>
            <Edit2 className="mr-2 h-4 w-4" />
            {isEditing ? 'Cancel' : 'Edit'}
          </Button>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4 space-y-6">
        {/* Profile Information */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5 text-primary" />
              Personal Information
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {isEditing ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="full_name">Full Name</Label>
                  <Input
                    id="full_name"
                    value={profileData.full_name}
                    onChange={(e) => setProfileData({ ...profileData, full_name: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Phone Number</Label>
                  <Input
                    id="phone"
                    type="tel"
                    value={profileData.phone}
                    onChange={(e) => setProfileData({ ...profileData, phone: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="date_of_birth">Date of Birth</Label>
                  <Input
                    id="date_of_birth"
                    type="date"
                    value={profileData.date_of_birth}
                    onChange={(e) => setProfileData({ ...profileData, date_of_birth: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="gender">Gender</Label>
                  <Input
                    id="gender"
                    value={profileData.gender}
                    onChange={(e) => setProfileData({ ...profileData, gender: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="language">Language</Label>
                  <Input
                    id="language"
                    value={profileData.language}
                    onChange={(e) => setProfileData({ ...profileData, language: e.target.value })}
                  />
                </div>
                <div className="md:col-span-2 flex gap-4">
                  <Button onClick={handleSaveProfile}>
                    Save Changes
                  </Button>
                  <Button variant="outline" onClick={() => setIsEditing(false)}>
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Name:</span>
                    <span className="font-medium">{profileData.full_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Email:</span>
                    <span className="font-medium">{profileData.email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Phone:</span>
                    <span className="font-medium">{profileData.phone || 'Not provided'}</span>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Date of Birth:</span>
                    <span className="font-medium">{profileData.date_of_birth || 'Not provided'}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Gender:</span>
                    <span className="font-medium">{profileData.gender || 'Not specified'}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Language:</span>
                    <Badge variant="outline">{profileData.language}</Badge>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Emergency Contacts */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5 text-primary" />
              Emergency Contacts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {emergencyContacts.map((contact) => (
                <div key={contact.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <div>
                    <p className="font-medium">{contact.name}</p>
                    <p className="text-sm text-muted-foreground capitalize">{contact.relationship}</p>
                    {contact.is_primary && (
                      <Badge variant="secondary" className="text-xs">Primary</Badge>
                    )}
                  </div>
                  <div className="text-right flex items-center gap-2">
                    <div>
                      <p className="font-medium">{contact.phone}</p>
                      {contact.email && (
                        <p className="text-sm text-muted-foreground">{contact.email}</p>
                      )}
                    </div>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="sm">
                        <Phone className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={() => deleteEmergencyContact(contact.id)}
                        className="text-destructive hover:text-destructive"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full" onClick={addEmergencyContact}>
                <Plus className="mr-2 h-4 w-4" />
                Add Emergency Contact
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Consultations */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-primary" />
              Booked Consultations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {consultations.map((consultation) => (
                <div key={consultation.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium">{consultation.doctor_name}</p>
                    <p className="text-sm text-muted-foreground">{consultation.doctor_specialty}</p>
                    {consultation.notes && (
                      <p className="text-xs text-muted-foreground mt-1">{consultation.notes}</p>
                    )}
                  </div>
                  <div className="text-center">
                    <p className="font-medium">{new Date(consultation.consultation_date).toLocaleDateString()}</p>
                    <p className="text-sm text-muted-foreground">{consultation.consultation_time}</p>
                  </div>
                  <Badge className={getStatusColor(consultation.status)}>
                    {consultation.status}
                  </Badge>
                </div>
              ))}
              {consultations.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Calendar className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No consultations scheduled</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Symptom Analysis History */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-primary" />
              Symptom Analysis History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {symptomHistory.map((analysis) => (
                <div key={analysis.id} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-medium">Predicted: {analysis.predicted_disease}</p>
                      <p className="text-sm text-muted-foreground">
                        Confidence: {analysis.confidence_score.toFixed(1)}%
                      </p>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {new Date(analysis.analysis_timestamp || '').toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-1 mb-2">
                    {analysis.symptoms.map((symptom, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">
                        {symptom}
                      </Badge>
                    ))}
                  </div>
                  {analysis.follow_up_required && (
                    <Badge variant="outline" className="text-orange-600 border-orange-600">
                      Follow-up Required
                    </Badge>
                  )}
                </div>
              ))}
              {symptomHistory.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Clock className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No symptom analysis history</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Medical Reports */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              Medical Reports
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center py-8">
              <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground mb-4">No medical reports uploaded</p>
              <Button variant="outline">
                <Upload className="mr-2 h-4 w-4" />
                Upload Report
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Settings & Logout */}
        <Card className="shadow-card-custom">
          <CardContent className="p-4">
            <div className="flex gap-4">
              <Button variant="outline" className="flex-1">
                <Settings className="mr-2 h-4 w-4" />
                Settings
              </Button>
              <Button 
                variant="outline" 
                className="flex-1 border-destructive text-destructive hover:bg-destructive hover:text-white"
                onClick={handleLogout}
              >
                <LogOut className="mr-2 h-4 w-4" />
                Logout
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Profile;