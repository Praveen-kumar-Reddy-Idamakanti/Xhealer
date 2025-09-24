import { useState } from 'react';
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
  Upload
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface EmergencyContact {
  name: string;
  relationship: string;
  phone: string;
}

interface Consultation {
  id: string;
  doctor: string;
  specialty: string;
  date: string;
  time: string;
  status: 'upcoming' | 'completed' | 'cancelled';
}

interface ChatHistory {
  id: string;
  date: string;
  symptoms: string[];
  prediction: string;
}

const Profile = () => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    phone: '+91-9876543210',
    age: 28,
    gender: 'Female',
    language: 'English'
  });

  const emergencyContacts: EmergencyContact[] = [
    { name: 'John Johnson', relationship: 'Spouse', phone: '+91-9876543211' },
    { name: 'Mary Johnson', relationship: 'Mother', phone: '+91-9876543212' }
  ];

  const consultations: Consultation[] = [
    {
      id: '1',
      doctor: 'Dr. Priya Sharma',
      specialty: 'Cardiologist',
      date: '2024-01-15',
      time: '2:30 PM',
      status: 'upcoming'
    },
    {
      id: '2',
      doctor: 'Dr. Rajesh Kumar',
      specialty: 'General Physician',
      date: '2023-12-20',
      time: '11:00 AM',
      status: 'completed'
    }
  ];

  const chatHistory: ChatHistory[] = [
    {
      id: '1',
      date: '2024-01-10',
      symptoms: ['headache', 'fever', 'fatigue'],
      prediction: 'Common Cold'
    },
    {
      id: '2',
      date: '2024-01-05',
      symptoms: ['chest pain', 'shortness of breath'],
      prediction: 'Anxiety'
    }
  ];

  const handleSaveProfile = () => {
    setIsEditing(false);
    // Save profile data logic here
  };

  const handleLogout = () => {
    navigate('/');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'upcoming': return 'bg-primary text-primary-foreground';
      case 'completed': return 'bg-accent text-accent-foreground';
      case 'cancelled': return 'bg-destructive text-destructive-foreground';
      default: return 'bg-muted text-muted-foreground';
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
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={profileData.name}
                    onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
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
                  <Label htmlFor="age">Age</Label>
                  <Input
                    id="age"
                    type="number"
                    value={profileData.age}
                    onChange={(e) => setProfileData({ ...profileData, age: parseInt(e.target.value) })}
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
                    <span className="font-medium">{profileData.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Email:</span>
                    <span className="font-medium">{profileData.email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Phone:</span>
                    <span className="font-medium">{profileData.phone}</span>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">Age:</span>
                    <span className="font-medium">{profileData.age} years</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Gender:</span>
                    <span className="font-medium">{profileData.gender}</span>
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
              {emergencyContacts.map((contact, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <div>
                    <p className="font-medium">{contact.name}</p>
                    <p className="text-sm text-muted-foreground">{contact.relationship}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium">{contact.phone}</p>
                    <Button variant="ghost" size="sm">
                      <Phone className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full">
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
                    <p className="font-medium">{consultation.doctor}</p>
                    <p className="text-sm text-muted-foreground">{consultation.specialty}</p>
                  </div>
                  <div className="text-center">
                    <p className="font-medium">{consultation.date}</p>
                    <p className="text-sm text-muted-foreground">{consultation.time}</p>
                  </div>
                  <Badge className={getStatusColor(consultation.status)}>
                    {consultation.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Chat History */}
        <Card className="shadow-card-custom">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-primary" />
              Symptom Analysis History
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {chatHistory.map((chat) => (
                <div key={chat.id} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <p className="font-medium">Analysis Result: {chat.prediction}</p>
                    <p className="text-sm text-muted-foreground">{chat.date}</p>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {chat.symptoms.map((symptom, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">
                        {symptom}
                      </Badge>
                    ))}
                  </div>
                </div>
              ))}
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