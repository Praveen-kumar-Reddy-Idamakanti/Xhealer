export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.5"
  }
  public: {
    Tables: {
      user_profiles: {
        Row: {
          id: string
          user_id: string | null
          user_type: 'authenticated' | 'guest'
          email: string
          full_name: string
          phone: string | null
          date_of_birth: string | null
          gender: string | null
          language: string | null
          profile_picture_url: string | null
          is_active: boolean | null
          created_at: string | null
          updated_at: string | null
        }
        Insert: {
          id?: string
          user_id?: string | null
          user_type?: 'authenticated' | 'guest'
          email: string
          full_name: string
          phone?: string | null
          date_of_birth?: string | null
          gender?: string | null
          language?: string | null
          profile_picture_url?: string | null
          is_active?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string | null
          user_type?: 'authenticated' | 'guest'
          email?: string
          full_name?: string
          phone?: string | null
          date_of_birth?: string | null
          gender?: string | null
          language?: string | null
          profile_picture_url?: string | null
          is_active?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
      }
      emergency_contacts: {
        Row: {
          id: string
          user_id: string
          name: string
          relationship: 'spouse' | 'parent' | 'child' | 'sibling' | 'friend' | 'other'
          phone: string
          email: string | null
          is_primary: boolean | null
          created_at: string | null
          updated_at: string | null
        }
        Insert: {
          id?: string
          user_id: string
          name: string
          relationship: 'spouse' | 'parent' | 'child' | 'sibling' | 'friend' | 'other'
          phone: string
          email?: string | null
          is_primary?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          name?: string
          relationship?: 'spouse' | 'parent' | 'child' | 'sibling' | 'friend' | 'other'
          phone?: string
          email?: string | null
          is_primary?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
      }
      consultations: {
        Row: {
          id: string
          user_id: string
          doctor_name: string
          doctor_specialty: string
          doctor_phone: string | null
          doctor_email: string | null
          consultation_date: string
          consultation_time: string
          status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled'
          notes: string | null
          prescription_url: string | null
          follow_up_date: string | null
          created_at: string | null
          updated_at: string | null
        }
        Insert: {
          id?: string
          user_id: string
          doctor_name: string
          doctor_specialty: string
          doctor_phone?: string | null
          doctor_email?: string | null
          consultation_date: string
          consultation_time: string
          status?: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled'
          notes?: string | null
          prescription_url?: string | null
          follow_up_date?: string | null
          created_at?: string | null
          updated_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          doctor_name?: string
          doctor_specialty?: string
          doctor_phone?: string | null
          doctor_email?: string | null
          consultation_date?: string
          consultation_time?: string
          status?: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled'
          notes?: string | null
          prescription_url?: string | null
          follow_up_date?: string | null
          created_at?: string | null
          updated_at?: string | null
        }
      }
      symptom_analysis_history: {
        Row: {
          id: string
          user_id: string
          symptoms: string[]
          predicted_disease: string
          confidence_score: number
          top_predictions: Json | null
          analysis_timestamp: string | null
          follow_up_required: boolean | null
          follow_up_notes: string | null
        }
        Insert: {
          id?: string
          user_id: string
          symptoms: string[]
          predicted_disease: string
          confidence_score: number
          top_predictions?: Json | null
          analysis_timestamp?: string | null
          follow_up_required?: boolean | null
          follow_up_notes?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          symptoms?: string[]
          predicted_disease?: string
          confidence_score?: number
          top_predictions?: Json | null
          analysis_timestamp?: string | null
          follow_up_required?: boolean | null
          follow_up_notes?: string | null
        }
      }
      health_reminders: {
        Row: {
          id: string
          user_id: string
          reminder_type: string
          title: string
          description: string | null
          reminder_date: string
          reminder_time: string | null
          is_completed: boolean | null
          is_recurring: boolean | null
          recurrence_pattern: string | null
          created_at: string | null
        }
        Insert: {
          id?: string
          user_id: string
          reminder_type: string
          title: string
          description?: string | null
          reminder_date: string
          reminder_time?: string | null
          is_completed?: boolean | null
          is_recurring?: boolean | null
          recurrence_pattern?: string | null
          created_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          reminder_type?: string
          title?: string
          description?: string | null
          reminder_date?: string
          reminder_time?: string | null
          is_completed?: boolean | null
          is_recurring?: boolean | null
          recurrence_pattern?: string | null
          created_at?: string | null
        }
      }
      user_preferences: {
        Row: {
          id: string
          user_id: string
          theme: string | null
          language: string | null
          notifications_enabled: boolean | null
          email_notifications: boolean | null
          sms_notifications: boolean | null
          emergency_alerts: boolean | null
          data_sharing_consent: boolean | null
          created_at: string | null
          updated_at: string | null
        }
        Insert: {
          id?: string
          user_id: string
          theme?: string | null
          language?: string | null
          notifications_enabled?: boolean | null
          email_notifications?: boolean | null
          sms_notifications?: boolean | null
          emergency_alerts?: boolean | null
          data_sharing_consent?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          theme?: string | null
          language?: string | null
          notifications_enabled?: boolean | null
          email_notifications?: boolean | null
          sms_notifications?: boolean | null
          emergency_alerts?: boolean | null
          data_sharing_consent?: boolean | null
          created_at?: string | null
          updated_at?: string | null
        }
      }
    }
    Views: {
      user_dashboard_data: {
        Row: {
          id: string
          user_id: string | null
          email: string
          full_name: string
          phone: string | null
          user_type: 'authenticated' | 'guest'
          created_at: string | null
          emergency_contacts_count: number | null
          consultations_count: number | null
          symptom_analyses_count: number | null
          active_reminders_count: number | null
        }
      }
    }
    Functions: {
      get_user_profile_complete: {
        Args: {
          user_uuid: string
        }
        Returns: Json
      }
    }
    Enums: {
      user_type: 'authenticated' | 'guest'
      consultation_status: 'scheduled' | 'completed' | 'cancelled' | 'rescheduled'
      emergency_contact_relationship: 'spouse' | 'parent' | 'child' | 'sibling' | 'friend' | 'other'
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
