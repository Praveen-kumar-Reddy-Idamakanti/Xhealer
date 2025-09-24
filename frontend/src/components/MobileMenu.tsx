import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { 
  Menu, 
  MessageCircle, 
  MapPin, 
  Stethoscope,
  User,
  LogOut,
  UserPlus
} from 'lucide-react';
import { supabase } from '@/integrations/supabase/client';

const MobileMenu = () => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    {
      title: 'Health Chat',
      description: 'AI symptom analysis',
      icon: MessageCircle,
      route: '/chat',
    },
    {
      title: 'Find Hospitals',
      description: 'Nearby medical facilities',
      icon: MapPin,
      route: '/hospitals',
    },
    {
      title: 'Consult Doctor',
      description: 'Book appointments',
      icon: Stethoscope,
      route: '/doctors',
    },
    {
      title: 'Profile',
      description: 'Your health profile',
      icon: User,
      route: '/profile',
    }
  ];

  const handleNavigation = (route: string) => {
    navigate(route);
    setIsOpen(false);
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    navigate('/login');
    setIsOpen(false);
  };

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-80 bg-gradient-ivory border-r-0">
        <div className="flex flex-col h-full">
          <div className="py-6">
            <h2 className="text-xl font-bold text-foreground mb-2">HealthCare AI</h2>
            <p className="text-sm text-muted-foreground">Your health companion</p>
          </div>
          
          <div className="flex-1 space-y-2">
            {menuItems.map((item, index) => (
              <Button
                key={index}
                variant="ghost"
                className="w-full justify-start h-16 px-4 hover:bg-gradient-grey rounded-lg"
                onClick={() => handleNavigation(item.route)}
              >
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary/10 rounded-full">
                    <item.icon className="h-5 w-5 text-primary" />
                  </div>
                  <div className="text-left">
                    <div className="font-medium">{item.title}</div>
                    <div className="text-xs text-muted-foreground">{item.description}</div>
                  </div>
                </div>
              </Button>
            ))}
          </div>

          <div className="border-t pt-4 space-y-2">
            <Button
              variant="ghost"
              className="w-full justify-start text-destructive hover:bg-destructive/10"
              onClick={handleSignOut}
            >
              <LogOut className="mr-3 h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default MobileMenu;