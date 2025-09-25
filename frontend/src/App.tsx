import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LanguageSelect from "./pages/LanguageSelect";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ChatBotPage from "./pages/ChatBotPage";
import HospitalsPage from "./pages/HospitalsPage";
import DoctorConsultation from "./pages/DoctorConsultation";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
// Import test utility for development
import "./utils/testEmailJS";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LanguageSelect />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chat" element={<ChatBotPage />} />
          <Route path="/hospitals" element={<HospitalsPage />} />
          <Route path="/doctors" element={<DoctorConsultation />} />
          <Route path="/profile" element={<Profile />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
