import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, Bot, User, Mic, MicOff, Loader2, ChevronDown } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isTyping?: boolean;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: `👋 **AI Health Assistant**\n\n🔍 **Ready to analyze your symptoms!**\n\n💡 **Features:**\n• Advanced AI symptom analysis\n• Medical information & explanations\n• Voice & text input support\n• Professional medical guidance\n\n⚠️ **Disclaimer:** For informational purposes only. Consult healthcare professionals for diagnosis.\n\n**How can I help you today?**`,
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
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
      content: '',
      isUser: false,
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
        await new Promise(resolve => setTimeout(resolve, 15));
        
        // Scroll to bottom during typing
        scrollToBottom();
      }
      
      // Pause between lines
      await new Promise(resolve => setTimeout(resolve, 80));
    }
    
    // Mark as finished typing
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, isTyping: false }
        : msg
    ));
  };

  // Initialize speech recognition
  useEffect(() => {
    console.log('Checking for speech recognition support...');
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
          console.log('Speech recognition started');
          setIsListening(true);
        };
        
        recognition.onresult = (event) => {
          console.log('Speech recognition result:', event.results[0][0].transcript);
          const transcript = event.results[0][0].transcript;
          setInputValue(transcript);
          setIsListening(false);
        };
        
        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
        };
        
        recognition.onend = () => {
          console.log('Speech recognition ended');
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
        setSpeechSupported(true);
        console.log('Speech recognition initialized successfully');
      } catch (error) {
        console.error('Error initializing speech recognition:', error);
        setSpeechSupported(false);
      }
    } else {
      console.log('Speech recognition not supported');
      setSpeechSupported(false);
    }
  }, []);

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
      .trim();
    
    // First, try to split by commas (most common natural language separator)
    let symptoms: string[] = [];
    
    if (cleanedInput.includes(',')) {
      symptoms = cleanedInput
        .split(',')
        .map(symptom => symptom.trim())
        .filter(symptom => symptom.length > 0);
    } else {
      // If no commas, try to split by common conjunctions
      const conjunctions = [' and ', ' with ', ' along with ', ' plus ', ' also '];
      let foundConjunction = false;
      
      for (const conjunction of conjunctions) {
        if (cleanedInput.includes(conjunction)) {
          symptoms = cleanedInput
            .split(conjunction)
            .map(s => s.trim())
            .filter(s => s.length > 0);
          foundConjunction = true;
          break;
        }
      }
      
      // If no conjunctions found, treat as single symptom
      if (!foundConjunction) {
        symptoms = [cleanedInput];
      }
    }
    
    // Clean each symptom
    symptoms = symptoms
      .map(symptom => {
        // Remove common filler words but keep medical terms
        return symptom
          .replace(/\b(a|an|the|some|mild|severe|bad|terrible|awful)\b/g, '')
          .replace(/[.!?]+$/, '') // Remove trailing punctuation
          .trim();
      })
      .filter(symptom => symptom.length > 0);
    
    return symptoms.join(';');
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    
    // Check if input is a greeting
    if (isGreeting(inputValue)) {
      const greetingResponse = generateGreetingResponse(inputValue);
      await createTypingMessage(greetingResponse, (Date.now() + 1).toString());
      setInputValue('');
      return;
    }
    
    // Parse the input to extract symptoms
    const parsedSymptoms = parseSymptoms(inputValue);
    console.log('🔍 CHAT INTERFACE DEBUG: Original input:', inputValue);
    console.log('🔍 CHAT INTERFACE DEBUG: Parsed symptoms:', parsedSymptoms);
    
    setInputValue('');
    setIsLoading(true);

    try {
      // DEBUG: Log frontend request
      console.log('🔍 CHAT INTERFACE DEBUG: Sending request to backend');
      console.log('🔍 CHAT INTERFACE DEBUG: Input value:', inputValue);
      
      const requestData = { 
        symptoms: parsedSymptoms,
        top_k: 3
      };
      
      console.log('🔍 CHAT INTERFACE DEBUG: Request data:', requestData);
      
      // Send request to backend API
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      console.log('🔍 CHAT INTERFACE DEBUG: Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ CHAT INTERFACE DEBUG: Response error:', errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('🔍 CHAT INTERFACE DEBUG: Response data:', data);
      
      // Create visually enhanced response with backend data
      const topPrediction = data.top_k_predictions[0];
      const medicalInfo = topPrediction?.medical_info;
      
      let responseContent = `**AI Analysis Complete**\n\n`;
      responseContent += `**Primary Diagnosis:** ${data.predicted_disease}\n`;
      responseContent += `**Confidence:** ${(data.confidence * 100).toFixed(1)}%\n\n`;
      
      if (medicalInfo) {
        responseContent += `**Medical Definition:**\n${medicalInfo.medical_definition}\n\n`;
        responseContent += `**Simple Explanation:**\n${medicalInfo.layman_explanation}\n\n`;
        responseContent += `**Body System:** ${medicalInfo.body_system}\n`;
        responseContent += `**Severity:** ${medicalInfo.severity_level}\n`;
        responseContent += `**Duration:** ${medicalInfo.duration}\n\n`;
      }
      
      responseContent += `**Top Predictions:**\n`;
      data.top_k_predictions.slice(0, 3).forEach((pred: any, index: number) => {
        const rank = index + 1;
        responseContent += `${rank}. ${pred.disease} (${pred.percentage.toFixed(1)}%)\n`;
      });
      
      responseContent += `\n---\n`;
      responseContent += `<span style="color: red;">**Medical Disclaimer:** This is for informational purposes only. Please consult a healthcare professional for proper diagnosis.</span>`;

      // Use typing animation for the response
      await createTypingMessage(responseContent, (Date.now() + 1).toString());
      
    } catch (error) {
      console.error('Error calling backend API:', error);
      
      // Visually enhanced fallback response with typing animation
      const fallbackContent = `**Analysis Temporarily Unavailable**\n\n**Issue:** Unable to connect to our AI analysis system\n\n**Recommendations:**\n• Try again in a few moments\n• Consult with a healthcare professional directly\n• Contact our support team if needed\n\n**Emergency:** If you have severe symptoms, please seek immediate medical attention.\n\n---\n<span style="color: red;">**Medical Disclaimer:** This analysis is for informational purposes only. Please consult a healthcare professional for proper diagnosis.</span>`;
      await createTypingMessage(fallbackContent, (Date.now() + 1).toString());
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-ivory rounded-lg shadow-soft">
      <div className="p-4 border-b bg-gradient-chat text-white rounded-t-lg">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Bot className="h-5 w-5" />
          AI Health Assistant
        </h3>
        <p className="text-sm opacity-90">Get instant health guidance</p>
      </div>

      <ScrollArea className="flex-1 p-4 relative">
        <div 
          ref={messagesContainerRef}
          className="space-y-4"
          onScroll={handleScroll}
        >
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              {!message.isUser && (
                <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-primary" />
                </div>
              )}
              
              <Card className={`max-w-[80%] ${message.isUser ? 'bg-primary text-primary-foreground' : 'bg-white'}`}>
                <CardContent className="p-3">
                  <div 
                    className="text-sm" 
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
                  <p className={`text-xs mt-1 ${message.isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'}`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </CardContent>
              </Card>

              {message.isUser && (
                <div className="w-8 h-8 bg-accent/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4 text-accent" />
                </div>
              )}
            </div>
          ))}
          
          {/* Auto-scroll target */}
          <div ref={messagesEndRef} />
          
          {/* Scroll to bottom button */}
          {showScrollButton && (
            <div className="absolute bottom-2 right-2">
              <Button
                onClick={scrollToBottom}
                size="sm"
                className="rounded-full shadow-lg bg-primary hover:bg-primary/90 h-8 w-8 p-0"
              >
                <ChevronDown className="h-4 w-4" />
              </Button>
            </div>
          )}
          
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-primary" />
              </div>
              <Card className="bg-white">
                <CardContent className="p-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </ScrollArea>

      <div className="p-4 border-t bg-white/50 rounded-b-lg">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe your symptoms or ask a health question..."
            className="flex-1 bg-white border-border/50"
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
            disabled={isLoading || !inputValue.trim()}
            className="bg-gradient-primary hover:opacity-90"
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
            <p className="text-sm text-emergency font-medium animate-pulse">
              🎤 Listening... Speak now
            </p>
          </div>
        )}
        
        <div className="mt-2 text-center">
          <p className="text-xs text-muted-foreground">
            AI advice is not a substitute for professional medical care
          </p>
          {!speechSupported && (
            <p className="text-xs text-orange-600 mt-1">
              ⚠️ Voice input not supported in this browser. Use Chrome or Edge for voice features.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;