import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Send, Mic, MicOff, Volume2, Loader2, ChevronDown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
  isTyping?: boolean;
}

interface Prediction {
  disease: string;
  confidence: number;
  urgency: 'low' | 'moderate' | 'high' | 'emergency';
  explainability: string[];
}

const ChatBotPage = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'bot',
      content: `👋 **Welcome to AI Health Assistant!**\n\n🔍 **What I can do:**\n• Analyze your symptoms using advanced AI\n• Provide medical information and explanations\n• Suggest when to see a healthcare professional\n• Support both text and voice input\n\n💡 **How to use:**\n• Type your symptoms in the chat box below\n• Or click the microphone to speak your symptoms\n• I'll analyze and provide comprehensive results\n\n⚠️ **Important:** This is for informational purposes only. Always consult with a healthcare professional for proper diagnosis.\n\n**How can I help you today?**`,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Function to scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to render message content with HTML and markdown formatting
  const renderMessageContent = (content: string) => {
    // Convert **text** to <strong>text</strong>
    let formattedContent = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert line breaks to <br> tags
    formattedContent = formattedContent.replace(/\n/g, '<br>');
    
    // Return as dangerouslySetInnerHTML for HTML rendering
    return { __html: formattedContent };
  };

  // Auto-scroll when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle scroll detection
  const handleScroll = () => {
    if (messagesContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current;
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
      setShowScrollButton(!isNearBottom);
    }
  };

  // Function to create typing animation for bot messages
  const createTypingMessage = async (content: string, messageId: string) => {
    const lines = content.split('\n');
    let currentContent = '';
    
    // Add the message with empty content first
    const typingMessage: Message = {
      id: messageId,
      role: 'bot',
      content: '',
      timestamp: new Date(),
      isTyping: true
    };
    
    setMessages(prev => [...prev, typingMessage]);
    
    // Type each line with a delay
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Add line with typing effect
      for (let j = 0; j <= line.length; j++) {
        currentContent = lines.slice(0, i).join('\n') + '\n' + line.slice(0, j);
        
        setMessages(prev => prev.map(msg => 
          msg.id === messageId 
            ? { ...msg, content: currentContent }
            : msg
        ));
        
        // Small delay between characters
        await new Promise(resolve => setTimeout(resolve, 20));
        
        // Scroll to bottom during typing
        scrollToBottom();
      }
      
      // Pause between lines
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Mark as finished typing
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, isTyping: false }
        : msg
    ));
  };

  // Function to get simulation data (fallback when API is not available)
  const getSimulationData = async (symptoms: string) => {
    // This simulates the backend processing
    const symptomMap: { [key: string]: any } = {
      'fever; headache; fatigue; muscle aches': {
        predicted_disease: 'Common Cold',
        confidence: 0.048,
        top_k_predictions: [
          { disease: 'Type 2 Diabetes Mellitus', percentage: 12.3 },
          { disease: 'Gastroenteritis (Stomach Flu)', percentage: 6.2 },
          { disease: 'Common Cold', percentage: 4.8 }
        ],
        input_symptoms: ['fever', 'headache', 'fatigue', 'muscle aches']
      },
      'cough; wheezing; shortness of breath; chest tightness': {
        predicted_disease: 'Bronchitis',
        confidence: 0.153,
        top_k_predictions: [
          { disease: 'Bronchitis', percentage: 15.3 },
          { disease: 'Asthma', percentage: 11.1 },
          { disease: 'Type 2 Diabetes Mellitus', percentage: 4.1 }
        ],
        input_symptoms: ['cough', 'wheezing', 'shortness of breath', 'chest tightness']
      },
      'nausea; vomiting; diarrhea; abdominal pain': {
        predicted_disease: 'Gastroenteritis (Stomach Flu)',
        confidence: 0.067,
        top_k_predictions: [
          { disease: 'Gastroenteritis (Stomach Flu)', percentage: 6.7 },
          { disease: 'Influenza (Flu)', percentage: 5.6 },
          { disease: 'Type 2 Diabetes Mellitus', percentage: 3.9 }
        ],
        input_symptoms: ['nausea', 'vomiting', 'diarrhea', 'abdominal pain']
      },
      'high fever; body aches; chills; fatigue': {
        predicted_disease: 'Influenza (Flu)',
        confidence: 0.220,
        top_k_predictions: [
          { disease: 'Influenza (Flu)', percentage: 22.0 },
          { disease: 'Pneumonia', percentage: 6.1 },
          { disease: 'Generalized Anxiety Disorder (GAD)', percentage: 4.6 }
        ],
        input_symptoms: ['high fever', 'body aches', 'chills', 'fatigue']
      }
    };

    // Check for exact match first
    if (symptomMap[symptoms]) {
      return symptomMap[symptoms];
    }

    // Check for partial matches
    for (const [key, value] of Object.entries(symptomMap)) {
      const keySymptoms = key.split('; ').map(s => s.toLowerCase());
      const inputSymptoms = symptoms.split('; ').map(s => s.toLowerCase());
      
      if (keySymptoms.some(symptom => inputSymptoms.some(input => input.includes(symptom) || symptom.includes(input)))) {
        return value;
      }
    }

    // Default fallback
    return {
      predicted_disease: 'Common Cold',
      confidence: 0.048,
      top_k_predictions: [
        { disease: 'Common Cold', percentage: 4.8 },
        { disease: 'Influenza (Flu)', percentage: 3.2 },
        { disease: 'Allergies', percentage: 2.1 }
      ],
      input_symptoms: symptoms.split('; ').map(s => s.trim())
    };
  };

  const mockPredictions: Prediction[] = [
    {
      disease: 'Common Cold',
      confidence: 85,
      urgency: 'low',
      explainability: ['runny nose', 'mild fever', 'fatigue']
    },
    {
      disease: 'Seasonal Allergies',
      confidence: 65,
      urgency: 'low',
      explainability: ['sneezing', 'watery eyes']
    },
    {
      disease: 'Viral Infection',
      confidence: 45,
      urgency: 'moderate',
      explainability: ['body aches', 'fever']
    }
  ];

  // Initialize speech recognition
  useEffect(() => {
    console.log('ChatBotPage: Checking for speech recognition support...');
    console.log('webkitSpeechRecognition in window:', 'webkitSpeechRecognition' in window);
    console.log('SpeechRecognition in window:', 'SpeechRecognition' in window);
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      try {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = () => {
          console.log('ChatBotPage: Speech recognition started');
          setIsListening(true);
        };
        
        recognition.onresult = (event) => {
          console.log('ChatBotPage: Speech recognition result:', event.results[0][0].transcript);
          const transcript = event.results[0][0].transcript;
          setInputText(transcript);
          setIsListening(false);
        };
        
        recognition.onerror = (event) => {
          console.error('ChatBotPage: Speech recognition error:', event.error);
          setIsListening(false);
        };
        
        recognition.onend = () => {
          console.log('ChatBotPage: Speech recognition ended');
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
        setSpeechSupported(true);
        console.log('ChatBotPage: Speech recognition initialized successfully');
      } catch (error) {
        console.error('ChatBotPage: Error initializing speech recognition:', error);
        setSpeechSupported(false);
      }
    } else {
      console.log('ChatBotPage: Speech recognition not supported');
      setSpeechSupported(false);
    }
  }, []);

  // Function to detect if input is a greeting
  const isGreeting = (input: string): boolean => {
    const greetingPatterns = [
      /^(hello|hi|hey|good morning|good afternoon|good evening|greetings|howdy)$/i,
      /^(how are you|how's it going|what's up|how do you do)$/i,
      /^(nice to meet you|pleased to meet you)$/i,
      /^(thanks|thank you|thank you very much)$/i,
      /^(bye|goodbye|see you later|farewell)$/i
    ];
    
    const cleanInput = input.toLowerCase().trim();
    return greetingPatterns.some(pattern => pattern.test(cleanInput));
  };

  // Function to generate appropriate greeting response
  const generateGreetingResponse = (input: string): string => {
    const cleanInput = input.toLowerCase().trim();
    
    if (/^(hello|hi|hey|greetings|howdy)$/i.test(cleanInput)) {
      return `**Hello!** 👋\n\nI'm your AI Health Assistant. I'm here to help you with health-related questions and symptom analysis.\n\n**How can I assist you today?**\n• Describe your symptoms for analysis\n• Ask health-related questions\n• Get information about medical conditions\n\n**Example:** "I have a cough and fever" or "What are the symptoms of flu?"`;
    }
    
    if (/^(good morning|good afternoon|good evening)$/i.test(cleanInput)) {
      return `**Good ${cleanInput.includes('morning') ? 'morning' : cleanInput.includes('afternoon') ? 'afternoon' : 'evening'}!** 🌅\n\nI'm your AI Health Assistant, ready to help with your health concerns.\n\n**What would you like to know?**\n• Symptom analysis and disease prediction\n• Health information and guidance\n• Medical condition explanations\n\n**Just describe your symptoms or ask a question!**`;
    }
    
    if (/^(how are you|how's it going|what's up|how do you do)$/i.test(cleanInput)) {
      return `**I'm doing well, thank you for asking!** 😊\n\nI'm your AI Health Assistant, and I'm here to help you with health-related questions and concerns.\n\n**I can help you with:**\n• Analyzing symptoms and predicting possible conditions\n• Explaining medical terms in simple language\n• Providing health information and guidance\n• Answering questions about diseases and treatments\n\n**What health concern can I help you with today?**`;
    }
    
    if (/^(nice to meet you|pleased to meet you)$/i.test(cleanInput)) {
      return `**Nice to meet you too!** 🤝\n\nI'm your AI Health Assistant, and I'm excited to help you with your health questions and concerns.\n\n**I specialize in:**\n• Symptom analysis using advanced AI technology\n• Disease prediction based on your symptoms\n• Medical information in easy-to-understand language\n• Health guidance and recommendations\n\n**Tell me about your symptoms or ask me anything health-related!**`;
    }
    
    if (/^(thanks|thank you|thank you very much)$/i.test(cleanInput)) {
      return `**You're very welcome!** 😊\n\nI'm always happy to help with your health questions and concerns.\n\n**Remember:**\n• I'm here 24/7 for your health questions\n• Always consult healthcare professionals for proper diagnosis\n• Don't hesitate to ask if you have more questions\n\n**Is there anything else I can help you with?**`;
    }
    
    if (/^(bye|goodbye|see you later|farewell)$/i.test(cleanInput)) {
      return `**Goodbye!** 👋\n\nThank you for using the AI Health Assistant. I hope I was able to help you today.\n\n**Take care of your health and remember:**\n• Always consult healthcare professionals for proper diagnosis\n• Don't ignore persistent or severe symptoms\n• Take care of yourself!\n\n**Feel free to come back anytime you have health questions!**`;
    }
    
    return `**Hello!** 👋\n\nI'm your AI Health Assistant. I'm here to help you with health-related questions and symptom analysis.\n\n**How can I assist you today?**`;
  };

  // Function to parse natural language symptoms into semicolon-separated format
  const parseSymptoms = (input: string): string => {
    // Remove common phrases and clean up the input
    let cleanedInput = input.toLowerCase()
      .replace(/^(i have|i'm having|i am having|i feel|i'm feeling|i am feeling|symptoms? are?|my symptoms? are?)/, '')
      .replace(/\b(and|with|along with|plus|also)\b/g, ';')
      .replace(/\b(,|\.|!|\?)\b/g, '')
      .trim();
    
    // Split by semicolons and clean each symptom
    const symptoms = cleanedInput
      .split(';')
      .map(symptom => symptom.trim())
      .filter(symptom => symptom.length > 0)
      .map(symptom => {
        // Remove common filler words
        return symptom.replace(/\b(a|an|the|some|mild|severe|bad|terrible|awful)\b/g, '').trim();
      })
      .filter(symptom => symptom.length > 0);
    
    // If no semicolons found, try to split by common conjunctions
    if (symptoms.length === 1) {
      const singleSymptom = symptoms[0];
      const conjunctions = [' and ', ' with ', ' along with ', ' plus ', ' also '];
      
      for (const conjunction of conjunctions) {
        if (singleSymptom.includes(conjunction)) {
          return singleSymptom.split(conjunction)
            .map(s => s.trim())
            .filter(s => s.length > 0)
            .join(';');
        }
      }
    }
    
    return symptoms.join(';');
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    
    // Check if input is a greeting
    if (isGreeting(inputText)) {
      const greetingResponse = generateGreetingResponse(inputText);
      await createTypingMessage(greetingResponse, (Date.now() + 1).toString());
      setInputText('');
      return;
    }
    
    // Parse the input to extract symptoms
    const parsedSymptoms = parseSymptoms(inputText);
    console.log('🔍 FRONTEND DEBUG: Original input:', inputText);
    console.log('🔍 FRONTEND DEBUG: Parsed symptoms:', parsedSymptoms);
    
    setIsLoading(true);
    setShowResults(false);

    try {
      // DEBUG: Log frontend request
      console.log('🔍 FRONTEND DEBUG: Sending request to backend');
      console.log('🔍 FRONTEND DEBUG: Input text:', inputText);
      
      const requestData = { 
        symptoms: parsedSymptoms,
        top_k: 3
      };
      
      console.log('🔍 FRONTEND DEBUG: Request data:', requestData);
      
      // Send request to backend API
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      console.log('🔍 FRONTEND DEBUG: Response status:', response.status);
      console.log('🔍 FRONTEND DEBUG: Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ FRONTEND DEBUG: Response error:', errorText);
        
        // Try to parse error response
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = JSON.parse(errorText);
          if (errorData.error) {
            errorMessage = errorData.error;
          }
        } catch (e) {
          // Use default error message
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('🔍 FRONTEND DEBUG: Response data:', data);
      
      // Create visually enhanced bot response with backend data
      const topPrediction = data.top_k_predictions[0];
      const medicalInfo = topPrediction?.medical_info;
      
      let botContent = `**Symptom Analysis Complete**\n\n`;
      botContent += `**Your Symptoms:** ${data.input_symptoms?.join(', ') || 'Unknown symptoms'}\n\n`;
      
      // Main prediction with visual emphasis
      botContent += `**Primary Diagnosis:**\n`;
      botContent += `**${data.predicted_disease}** (${(data.confidence * 100).toFixed(1)}% confidence)\n\n`;
      
      if (medicalInfo) {
        // Medical information
        botContent += `**Medical Information:**\n`;
        botContent += `**Definition:** ${medicalInfo.medical_definition}\n\n`;
        botContent += `**In Simple Terms:** ${medicalInfo.layman_explanation}\n\n`;
        
        // Key details
        botContent += `**Key Details:**\n`;
        botContent += `**Body System:** ${medicalInfo.body_system}\n`;
        botContent += `**Severity:** ${medicalInfo.severity_level}\n`;
        botContent += `**Duration:** ${medicalInfo.duration}\n\n`;
        
        if (medicalInfo.common_symptoms?.length > 0) {
          botContent += `**Common Symptoms:**\n`;
          medicalInfo.common_symptoms.slice(0, 5).forEach((symptom: string, index: number) => {
            botContent += `• ${symptom}\n`;
          });
          botContent += `\n`;
        }
        
        if (medicalInfo.when_to_see_doctor?.length > 0) {
          botContent += `**When to See a Doctor:**\n`;
          medicalInfo.when_to_see_doctor.slice(0, 3).forEach((indicator: string, index: number) => {
            botContent += `• ${indicator}\n`;
          });
          botContent += `\n`;
        }
      }
      
      // Top predictions
      botContent += `**Top 3 Predictions:**\n`;
      data.top_k_predictions.slice(0, 3).forEach((pred: any, index: number) => {
        const rank = index + 1;
        botContent += `${rank}. **${pred.disease}** (${pred.percentage.toFixed(1)}%)\n`;
      });
      
      botContent += `\n---\n`;
      botContent += `<span style="color: red;">**Medical Disclaimer:** This analysis is for informational purposes only. Always consult with a healthcare professional for proper diagnosis and treatment.</span>`;

      // Use typing animation for the response
      await createTypingMessage(botContent, (Date.now() + 1).toString());
      
      // Convert backend response to frontend format for detailed view
      const formattedPredictions: Prediction[] = data.top_k_predictions.map((pred: any, index: number) => ({
        disease: pred.disease,
        confidence: pred.percentage,
        urgency: pred.urgency_level || (pred.percentage > 70 ? 'high' : pred.percentage > 40 ? 'moderate' : 'low'),
        explainability: data.input_symptoms || []
      }));
      
      setPredictions(formattedPredictions);
      setShowResults(true);
      
    } catch (error) {
      console.error('Error calling backend API:', error);
      
      // Show visually enhanced error message with typing animation
      const errorContent = `**Analysis Issue Detected**\n\n**Problem:** ${error instanceof Error ? error.message : 'Unknown error'}\n\n**Solution:** Switching to backup analysis system...\n\nPlease wait while I process your symptoms...`;
      await createTypingMessage(errorContent, (Date.now() + 1).toString());
      
      // Use our working simulation data as fallback
      try {
        const simulationData = await getSimulationData(inputText);
        
        const backupContent = `**Backup Analysis Results**\n\n**Your Symptoms:** ${simulationData.input_symptoms?.join(', ') || inputText}\n\n**Most Likely Condition:** ${simulationData.predicted_disease}\n**Confidence:** ${(simulationData.confidence * 100).toFixed(1)}%\n\n**Top Predictions:**\n${simulationData.top_k_predictions.map((pred: any, index: number) => {
          const rank = index + 1;
          return `${rank}. ${pred.disease} (${pred.percentage.toFixed(1)}%)`;
        }).join('\n')}\n\n---\n<span style="color: red;">**Medical Disclaimer:** This is a backup analysis. Please consult a healthcare professional for proper diagnosis.</span>`;
        
        await createTypingMessage(backupContent, (Date.now() + 2).toString());
        
        // Convert simulation data to frontend format
        const formattedPredictions: Prediction[] = simulationData.top_k_predictions.map((pred: any, index: number) => ({
          disease: pred.disease,
          confidence: pred.percentage,
          urgency: pred.percentage > 70 ? 'high' : pred.percentage > 40 ? 'moderate' : 'low',
          explainability: simulationData.input_symptoms || []
        }));
        
        setPredictions(formattedPredictions);
        setShowResults(true);
      } catch (fallbackError) {
        console.error('Fallback analysis also failed:', fallbackError);

        const finalErrorContent = `😔 **Analysis Unavailable**\n\n🚫 **Issue:** Unable to process your symptoms at this time\n\n💡 **Recommendations:**\n• Try again in a few moments\n• Consult with a healthcare professional directly\n• Contact our support team if the issue persists\n\n🏥 **Emergency:** If you have severe symptoms, please seek immediate medical attention.`;
        await createTypingMessage(finalErrorContent, (Date.now() + 3).toString());
      }
    } finally {
      setIsLoading(false);
    setInputText('');
    }
  };

  const toggleListening = () => {
    if (!speechSupported || !recognitionRef.current) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
    }
  };

  const speakResult = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthesis.speak(utterance);
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'low': return 'bg-accent text-accent-foreground';
      case 'moderate': return 'bg-orange-500 text-white';
      case 'high': return 'bg-destructive text-destructive-foreground';
      case 'emergency': return 'bg-emergency text-emergency-foreground';
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
          <div>
            <h1 className="text-xl font-semibold">Health Assistant</h1>
            <p className="text-sm text-muted-foreground">AI-powered symptom analysis</p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4">
        {/* Chat Messages */}
        <Card className="shadow-card-custom mb-4">
          <CardContent className="p-4 relative">
            <div 
              ref={messagesContainerRef}
              className="space-y-4 max-h-96 overflow-y-auto"
              onScroll={handleScroll}
            >
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted text-muted-foreground'
                    }`}
                  >
                    <div 
                      dangerouslySetInnerHTML={renderMessageContent(message.content)}
                    />
                    {message.isTyping && (
                      <div className="flex items-center gap-1 mt-1">
                        <div className="w-1 h-1 bg-primary rounded-full animate-pulse"></div>
                        <div className="w-1 h-1 bg-primary rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                        <div className="w-1 h-1 bg-primary rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                        <span className="text-xs text-muted-foreground ml-2">AI is typing...</span>
                      </div>
                    )}
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {/* Auto-scroll target */}
              <div ref={messagesEndRef} />
            </div>
            
            {/* Scroll to bottom button */}
            {showScrollButton && (
              <div className="absolute bottom-4 right-4">
                <Button
                  onClick={scrollToBottom}
                  size="sm"
                  className="rounded-full shadow-lg bg-primary hover:bg-primary/90"
                >
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Analysis Results */}
        {showResults && (
          <Card className="shadow-card-custom mb-4">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                Analysis Results
                <Badge variant="secondary">{predictions.length} matches found</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {predictions.map((prediction, index) => (
                  <div key={index} className="border rounded-lg p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-lg">{prediction.disease}</h3>
                      <div className="flex items-center gap-2">
                        <Badge className={getUrgencyColor(prediction.urgency)}>
                          {prediction.urgency}
                        </Badge>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => speakResult(`${prediction.disease} with ${prediction.confidence}% confidence`)}
                        >
                          <Volume2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium">Confidence</span>
                          <span className="text-sm font-medium">{prediction.confidence}%</span>
                        </div>
                        <div className="w-full bg-muted rounded-full h-2">
                          <div
                            className="bg-primary h-2 rounded-full transition-all"
                            style={{ width: `${prediction.confidence}%` }}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium mb-2">Key symptoms identified:</p>
                      <div className="flex flex-wrap gap-1">
                        {prediction.explainability.map((symptom, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs">
                            {symptom}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
                
                <div className="mt-6 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                  <p className="text-sm text-orange-800 font-medium">
                    ⚠️ Medical Disclaimer: This analysis is for informational purposes only. 
                    Always consult with a healthcare professional for proper diagnosis and treatment.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Input Area */}
        <Card className="shadow-card-custom">
          <CardContent className="p-4">
            <div className="flex gap-2">
              <Input
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Describe your symptoms or click mic to speak..."
                onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
                className="flex-1"
                disabled={isLoading}
              />
              <Button
                variant={isListening ? "default" : "outline"}
                size="icon"
                onClick={toggleListening}
                className={isListening ? "bg-emergency animate-pulse" : ""}
                disabled={isLoading}
                title={isListening ? "Stop listening" : speechSupported ? "Start voice input" : "Voice input not supported"}
              >
                {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              </Button>
              <Button 
                onClick={handleSendMessage} 
                disabled={!inputText.trim() || isLoading}
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
            
            {isListening && (
              <div className="mt-2 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <div className="w-2 h-2 bg-emergency rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-emergency rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 bg-emergency rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                </div>
                <p className="text-sm text-emergency font-medium animate-pulse">
                  🎤 Listening... Speak your symptoms now
                </p>
              </div>
            )}
            
            {isLoading && (
              <div className="mt-2 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
                <p className="text-sm text-primary font-medium">
                  🔍 AI is analyzing your symptoms...
                </p>
              </div>
            )}
            
            {!speechSupported && (
              <div className="mt-2 p-2 bg-orange-50 border border-orange-200 rounded-lg">
                <p className="text-xs text-orange-700 flex items-center gap-1">
                  ⚠️ Voice input not supported in this browser. Use Chrome or Edge for voice features.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ChatBotPage;