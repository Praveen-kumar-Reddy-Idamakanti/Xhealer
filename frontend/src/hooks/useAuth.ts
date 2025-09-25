import { useState, useEffect } from 'react';
import { User } from '@supabase/supabase-js';
import { supabase } from '@/integrations/supabase/client';
import { Database } from '@/integrations/supabase/types';

type UserProfile = Database['public']['Tables']['user_profiles']['Row'];
type UserType = 'authenticated' | 'guest' | null;

interface AuthState {
  user: User | null;
  profile: UserProfile | null;
  userType: UserType;
  loading: boolean;
  isGuest: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    profile: null,
    userType: null,
    loading: true,
    isGuest: false,
  });

  useEffect(() => {
    // Get initial session
    const getInitialSession = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession();
        
        if (session?.user) {
          await loadUserProfile(session.user);
        } else {
          // Check if user is guest (stored in localStorage)
          const isGuest = localStorage.getItem('isGuest') === 'true';
          setAuthState({
            user: null,
            profile: null,
            userType: isGuest ? 'guest' : null,
            loading: false,
            isGuest: isGuest,
          });
        }
      } catch (error) {
        console.error('Error getting initial session:', error);
        setAuthState({
          user: null,
          profile: null,
          userType: null,
          loading: false,
          isGuest: false,
        });
      }
    };

    getInitialSession();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth state change:', event, session?.user?.id);
        if (session?.user) {
          await loadUserProfile(session.user);
        } else {
          // Check if user is guest
          const isGuest = localStorage.getItem('isGuest') === 'true';
          setAuthState({
            user: null,
            profile: null,
            userType: isGuest ? 'guest' : null,
            loading: false,
            isGuest: isGuest,
          });
        }
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const loadUserProfile = async (user: User) => {
    try {
      console.log('Loading profile for user:', user.id);
      
      // First check if the table exists by trying a simple query
      const { error: tableError } = await supabase
        .from('user_profiles')
        .select('id')
        .limit(1);
        
      if (tableError) {
        console.error('Database table error:', tableError);
        // If table doesn't exist, set user without profile
        setAuthState({
          user,
          profile: null,
          userType: 'authenticated',
          loading: false,
          isGuest: false,
        });
        return;
      }
      
      // Get user profile
      const { data: profile, error } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', user.id)
        .single();

      if (error) {
        if (error.code === 'PGRST116') { // PGRST116 = no rows returned
          console.log('No profile found, creating new profile...');
          // Create a new profile if none exists
          const newProfile = {
            user_id: user.id,
            email: user.email || '',
            full_name: user.user_metadata?.full_name || user.email?.split('@')[0] || 'User',
            user_type: 'authenticated' as const
          };
          
          const { data: createdProfile, error: createError } = await supabase
            .from('user_profiles')
            .insert(newProfile)
            .select()
            .single();
            
          if (createError) {
            console.error('Error creating profile:', createError);
            setAuthState({
              user,
              profile: null,
              userType: 'authenticated',
              loading: false,
              isGuest: false,
            });
            return;
          }
          
          setAuthState({
            user,
            profile: createdProfile,
            userType: 'authenticated',
            loading: false,
            isGuest: false,
          });
          return;
        } else {
          console.error('Error loading profile:', error);
        }
      }

      console.log('Profile loaded:', profile);
      setAuthState({
        user,
        profile,
        userType: 'authenticated',
        loading: false,
        isGuest: false,
      });
    } catch (error) {
      console.error('Error loading user profile:', error);
      setAuthState({
        user,
        profile: null,
        userType: 'authenticated',
        loading: false,
        isGuest: false,
      });
    }
  };

  const signInAsGuest = () => {
    localStorage.setItem('isGuest', 'true');
    setAuthState({
      user: null,
      profile: null,
      userType: 'guest',
      loading: false,
      isGuest: true,
    });
  };

  const signOut = async () => {
    if (authState.isGuest) {
      localStorage.removeItem('isGuest');
    } else {
      await supabase.auth.signOut();
    }
    
    setAuthState({
      user: null,
      profile: null,
      userType: null,
      loading: false,
      isGuest: false,
    });
  };

  const updateProfile = async (updates: Partial<UserProfile>) => {
    if (!authState.user || !authState.profile) return;

    try {
      const { data, error } = await supabase
        .from('user_profiles')
        .update(updates)
        .eq('id', authState.profile.id)
        .select()
        .single();

      if (error) throw error;

      setAuthState(prev => ({
        ...prev,
        profile: data,
      }));

      return data;
    } catch (error) {
      console.error('Error updating profile:', error);
      throw error;
    }
  };

  const createProfile = async (profileData: {
    email: string;
    full_name: string;
    phone?: string;
    date_of_birth?: string;
    gender?: string;
    language?: string;
  }) => {
    if (!authState.user) return;

    try {
      const { data, error } = await supabase
        .from('user_profiles')
        .insert({
          user_id: authState.user.id,
          user_type: 'authenticated',
          ...profileData,
        })
        .select()
        .single();

      if (error) throw error;

      setAuthState(prev => ({
        ...prev,
        profile: data,
      }));

      return data;
    } catch (error) {
      console.error('Error creating profile:', error);
      throw error;
    }
  };

  return {
    ...authState,
    signInAsGuest,
    signOut,
    updateProfile,
    createProfile,
    loadUserProfile,
  };
};
