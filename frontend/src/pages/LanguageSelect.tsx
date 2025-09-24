import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Languages, Globe } from 'lucide-react';

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
  { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
  { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
];

const LanguageSelect = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const navigate = useNavigate();

  const handleContinue = () => {
    localStorage.setItem('selectedLanguage', selectedLanguage);
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-card-custom">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 p-3 bg-primary/10 rounded-full w-fit">
            <Globe className="h-8 w-8 text-primary" />
          </div>
          <CardTitle className="text-2xl font-bold">Choose Your Language</CardTitle>
          <CardDescription>
            Select your preferred language to continue
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-3">
            {languages.map((lang) => (
              <Button
                key={lang.code}
                variant={selectedLanguage === lang.code ? "default" : "outline"}
                className="justify-start h-12 text-left"
                onClick={() => setSelectedLanguage(lang.code)}
              >
                <span className="mr-3 text-lg">{lang.flag}</span>
                <span className="font-medium">{lang.name}</span>
              </Button>
            ))}
          </div>
          <Button 
            className="w-full mt-6" 
            onClick={handleContinue}
          >
            <Languages className="mr-2 h-4 w-4" />
            Continue
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default LanguageSelect;