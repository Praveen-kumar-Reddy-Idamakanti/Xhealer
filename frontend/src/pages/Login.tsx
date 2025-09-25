import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Shield } from 'lucide-react';
import { supabase } from '@/integrations/supabase/client';
import { useAuth } from '@/hooks/useAuth';
import medicalHero from '@/assets/medical-hero.jpg';

const Login = () => {
  const navigate = useNavigate();
  const { user, isGuest, loading } = useAuth();

  useEffect(() => {
    // Redirect if already authenticated or guest
    if (!loading && (user || isGuest)) {
      navigate('/dashboard');
    }
  }, [user, isGuest, loading, navigate]);

  const handleGoogleLogin = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/dashboard`
      }
    });

    if (error) {
      console.error('Error logging in:', error.message);
    }
  };

  const { signInAsGuest } = useAuth();

  const handleGuestLogin = () => {
    signInAsGuest();
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-background flex">
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-chat relative overflow-hidden">
        <img 
          src={medicalHero} 
          alt="Medical Healthcare" 
          className="absolute inset-0 w-full h-full object-cover mix-blend-overlay"
        />
        <div className="relative z-10 p-12 flex flex-col justify-center text-white">
          <h1 className="text-4xl font-bold mb-4">HealthCare AI</h1>
          <p className="text-xl opacity-90 mb-6">
            Your trusted medical companion powered by advanced AI technology
          </p>
          <div className="space-y-2 opacity-80">
            <p className="flex items-center gap-2">✓ 24/7 AI Health Assistant</p>
            <p className="flex items-center gap-2">✓ Find Nearby Hospitals</p>
            <p className="flex items-center gap-2">✓ Doctor Consultations</p>
            <p className="flex items-center gap-2">✓ Emergency Services</p>
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4 bg-gradient-ivory">
        <Card className="w-full max-w-md shadow-soft bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 p-3 bg-gradient-primary rounded-full w-fit">
              <Shield className="h-8 w-8 text-white" />
            </div>
            <CardTitle className="text-2xl font-bold text-foreground">Welcome to HealthCare AI</CardTitle>
            <CardDescription className="text-muted-foreground">
              Choose your preferred way to access your health dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button 
              className="w-full bg-gradient-primary hover:opacity-90" 
              onClick={handleGoogleLogin}
              size="lg"
            >
              <svg className="mr-2 h-4 w-4" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Continue with Google
            </Button>
            
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border/50" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-muted-foreground">Or</span>
              </div>
            </div>

            <Button 
              variant="outline" 
              className="w-full border-primary/30 hover:bg-gradient-grey" 
              onClick={handleGuestLogin}
              size="lg"
            >
              Continue as Guest
            </Button>
            
            <p className="text-xs text-center text-muted-foreground mt-4">
              Guest access provides limited functionality. Sign in with Google for full features and data sync.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Login;