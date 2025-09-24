import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { ArrowLeft, Star, Clock, Video, Phone, Calendar, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Doctor {
  id: string;
  name: string;
  specialty: string;
  qualifications: string;
  experience: number;
  rating: number;
  language: string[];
  consultationFee: number;
  availableToday: boolean;
  nextSlot: string;
  telemedicineEnabled: boolean;
  profileImage?: string;
}

interface TimeSlot {
  time: string;
  available: boolean;
}

const DoctorConsultation = () => {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);
  const [isBookingOpen, setIsBookingOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const mockDoctors: Doctor[] = [
    {
      id: '1',
      name: 'Dr. Priya Sharma',
      specialty: 'Cardiologist',
      qualifications: 'MBBS, MD (Cardiology)',
      experience: 15,
      rating: 4.8,
      language: ['English', 'Hindi'],
      consultationFee: 800,
      availableToday: true,
      nextSlot: '2:30 PM',
      telemedicineEnabled: true
    },
    {
      id: '2',
      name: 'Dr. Rajesh Kumar',
      specialty: 'General Physician',
      qualifications: 'MBBS, MD (Internal Medicine)',
      experience: 12,
      rating: 4.6,
      language: ['English', 'Hindi', 'Telugu'],
      consultationFee: 500,
      availableToday: true,
      nextSlot: '11:00 AM',
      telemedicineEnabled: true
    },
    {
      id: '3',
      name: 'Dr. Anita Reddy',
      specialty: 'Gynecologist',
      qualifications: 'MBBS, MS (Obstetrics & Gynecology)',
      experience: 18,
      rating: 4.9,
      language: ['English', 'Telugu', 'Tamil'],
      consultationFee: 900,
      availableToday: false,
      nextSlot: 'Tomorrow 10:00 AM',
      telemedicineEnabled: true
    },
    {
      id: '4',
      name: 'Dr. Vikram Singh',
      specialty: 'Orthopedist',
      qualifications: 'MBBS, MS (Orthopedics)',
      experience: 10,
      rating: 4.5,
      language: ['English', 'Hindi'],
      consultationFee: 700,
      availableToday: true,
      nextSlot: '4:00 PM',
      telemedicineEnabled: false
    }
  ];

  useState(() => {
    setDoctors(mockDoctors);
  });

  const timeSlots: TimeSlot[] = [
    { time: '10:00 AM', available: true },
    { time: '10:30 AM', available: false },
    { time: '11:00 AM', available: true },
    { time: '11:30 AM', available: true },
    { time: '02:00 PM', available: false },
    { time: '02:30 PM', available: true },
    { time: '03:00 PM', available: true },
    { time: '03:30 PM', available: false },
  ];

  const filteredDoctors = doctors.filter(doctor =>
    doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleBookAppointment = (doctor: Doctor) => {
    setSelectedDoctor(doctor);
    setIsBookingOpen(true);
  };

  const confirmBooking = () => {
    if (selectedDoctor && selectedDate && selectedTime) {
      alert(`Appointment booked with ${selectedDoctor.name} on ${selectedDate} at ${selectedTime}`);
      setIsBookingOpen(false);
      setSelectedDoctor(null);
      setSelectedDate('');
      setSelectedTime('');
    }
  };

  const handleCall = (doctorName: string) => {
    alert(`Calling ${doctorName}...`);
  };

  const handleVideoCall = (doctorName: string) => {
    alert(`Starting video consultation with ${doctorName}...`);
  };

  return (
    <div className="min-h-screen bg-gradient-background">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-xl font-semibold">Doctor Consultation</h1>
            <p className="text-sm text-muted-foreground">Book appointments with verified doctors</p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4 space-y-4">
        {/* Search Bar */}
        <Card className="shadow-card-custom">
          <CardContent className="p-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search doctors or specialties..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Doctors List */}
        <div className="space-y-4">
          {filteredDoctors.map((doctor) => (
            <Card key={doctor.id} className="shadow-card-custom">
              <CardContent className="p-6">
                <div className="flex flex-col lg:flex-row gap-6">
                  {/* Doctor Info */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                        <span className="text-primary font-semibold text-lg">
                          {doctor.name.charAt(0)}
                        </span>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">{doctor.name}</h3>
                        <p className="text-primary font-medium">{doctor.specialty}</p>
                        <p className="text-sm text-muted-foreground">{doctor.qualifications}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Experience</p>
                        <p className="font-medium">{doctor.experience} years</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Rating</p>
                        <div className="flex items-center gap-1">
                          <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                          <span className="font-medium">{doctor.rating}</span>
                        </div>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Fee</p>
                        <p className="font-medium">₹{doctor.consultationFee}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Next Available</p>
                        <p className="font-medium">{doctor.nextSlot}</p>
                      </div>
                    </div>

                    <div className="mt-3">
                      <p className="text-sm text-muted-foreground mb-2">Languages:</p>
                      <div className="flex flex-wrap gap-1">
                        {doctor.language.map((lang, idx) => (
                          <Badge key={idx} variant="outline">
                            {lang}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div className="flex gap-2 mt-3">
                      {doctor.availableToday && (
                        <Badge className="bg-accent text-accent-foreground">
                          Available Today
                        </Badge>
                      )}
                      {doctor.telemedicineEnabled && (
                        <Badge variant="secondary">
                          Video Consultation
                        </Badge>
                      )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="lg:w-48 space-y-3">
                    <Button
                      className="w-full"
                      onClick={() => handleBookAppointment(doctor)}
                    >
                      <Calendar className="mr-2 h-4 w-4" />
                      Book Appointment
                    </Button>

                    {doctor.telemedicineEnabled && (
                      <Button
                        variant="outline"
                        className="w-full"
                        onClick={() => handleVideoCall(doctor.name)}
                      >
                        <Video className="mr-2 h-4 w-4" />
                        Video Call
                      </Button>
                    )}

                    <Button
                      variant="outline"
                      className="w-full"
                      onClick={() => handleCall(doctor.name)}
                    >
                      <Phone className="mr-2 h-4 w-4" />
                      Call Clinic
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredDoctors.length === 0 && (
          <Card className="shadow-card-custom">
            <CardContent className="p-8 text-center">
              <Search className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">No doctors found matching your search.</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Booking Modal */}
      <Dialog open={isBookingOpen} onOpenChange={setIsBookingOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Book Appointment</DialogTitle>
          </DialogHeader>
          
          {selectedDoctor && (
            <div className="space-y-4">
              <div className="text-center">
                <h3 className="font-semibold">{selectedDoctor.name}</h3>
                <p className="text-sm text-muted-foreground">{selectedDoctor.specialty}</p>
                <p className="text-sm font-medium">Fee: ₹{selectedDoctor.consultationFee}</p>
              </div>

              <div>
                <label className="text-sm font-medium">Select Date</label>
                <Input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>

              <div>
                <label className="text-sm font-medium">Select Time</label>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {timeSlots.map((slot, index) => (
                    <Button
                      key={index}
                      variant={selectedTime === slot.time ? "default" : "outline"}
                      size="sm"
                      disabled={!slot.available}
                      onClick={() => setSelectedTime(slot.time)}
                    >
                      <Clock className="mr-1 h-3 w-3" />
                      {slot.time}
                    </Button>
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <Button variant="outline" className="flex-1" onClick={() => setIsBookingOpen(false)}>
                  Cancel
                </Button>
                <Button 
                  className="flex-1" 
                  onClick={confirmBooking}
                  disabled={!selectedDate || !selectedTime}
                >
                  Confirm Booking
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default DoctorConsultation;