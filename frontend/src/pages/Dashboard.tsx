import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  MessageCircle, 
  MapPin, 
  Phone, 
  Stethoscope,
  AlertTriangle,
  User,
  Bell,
  TrendingUp
} from 'lucide-react';
import SOSButton from '@/components/SOSButton';
import MobileMenu from '@/components/MobileMenu';
import ChatInterface from '@/components/ChatInterface';
import { useIsMobile } from '@/hooks/use-mobile';

const Dashboard = () => {
  const navigate = useNavigate();
  const isMobile = useIsMobile();
  const [userName] = useState('Sarah');

  const quickActions = [
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
    }
  ];

  const healthInsights = [
    { 
      title: 'Health Tips', 
      content: 'Stay hydrated and get 7-8 hours of sleep daily',
      icon: TrendingUp,
      color: 'bg-gradient-health'
    },
    { 
      title: 'Reminders', 
      content: 'Annual checkup due next month',
      icon: Bell,
      color: 'bg-gradient-primary'
    }
  ];

  if (isMobile) {
    return (
      <div className="min-h-screen bg-gradient-background">
        {/* Mobile Header */}
        <div className="bg-gradient-ivory shadow-soft border-b">
          <div className="px-4 py-4 flex justify-between items-center">
            <MobileMenu />
            <div className="text-center">
              <h1 className="text-lg font-bold text-foreground">HealthCare AI</h1>
            </div>
            <Button variant="ghost" size="icon" onClick={() => navigate('/profile')}>
              <User className="h-5 w-5" />
            </Button>
          </div>
        </div>

        {/* Mobile Chat Interface - 100% of screen */}
        <div className="h-[calc(100vh-80px)] p-4">
          <ChatInterface />
        </div>

        {/* Floating SOS Button */}
        <SOSButton />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-background">
      {/* Desktop Header */}
      <div className="bg-gradient-ivory shadow-soft border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Good Morning, {userName}</h1>
            <p className="text-muted-foreground">Your AI health companion is ready to help</p>
          </div>
          <Button variant="ghost" size="icon" onClick={() => navigate('/profile')}>
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Interface - 70% */}
          <div className="lg:col-span-2">
            <div className="h-[600px]">
              <ChatInterface />
            </div>
          </div>

          {/* Side Panel - 30% */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card className="shadow-soft bg-gradient-ivory">
              <CardHeader>
                <CardTitle className="text-xxl mt-12">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {quickActions.map((action, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    className="w-full justify-start h-14 hover:bg-gradient-grey transition-all"
                    onClick={() => navigate(action.route)}
                  >
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-primary/10 rounded-full">
                        <action.icon className="h-5 w-5 text-primary" />
                      </div>
                      <div className="text-left">
                        <div className="font-medium text-sm">{action.title}</div>
                        <div className="text-xs text-muted-foreground">{action.description}</div>
                      </div>
                    </div>
                  </Button>
                ))}
              </CardContent>
            </Card>

            {/* Health Insights */}
            <Card className="shadow-soft bg-gradient-ivory">
              <CardHeader>
                <CardTitle className="text-xxl mt-12">Health Insights</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {healthInsights.map((insight, index) => (
                  <div key={index} className="p-3 rounded-lg bg-white/60 border">
                    <div className="flex items-start space-x-3">
                      <div className={`p-2 rounded-full ${insight.color} text-white`}>
                        <insight.icon className="h-4 w-4" />
                      </div>
                      <div>
                        <h4 className="font-medium text-sm">{insight.title}</h4>
                        <p className="text-xs text-muted-foreground mt-1">{insight.content}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Emergency Section */}
                

            {/* Recent Activity */}
            
          </div>
        </div>
      </div>

      {/* Floating SOS Button */}
      <SOSButton />
    </div>
  );
};

export default Dashboard;