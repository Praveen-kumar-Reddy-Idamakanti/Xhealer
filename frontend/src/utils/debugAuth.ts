import { supabase } from '@/integrations/supabase/client';

/**
 * Debug utility to check authentication and database connection
 */
export const debugAuth = async () => {
  console.log('🔍 Debugging Authentication and Database Connection...');
  
  try {
    // Check Supabase client
    console.log('✓ Supabase client initialized');
    
    // Check current session
    const { data: { session }, error: sessionError } = await supabase.auth.getSession();
    console.log('Session:', session);
    if (sessionError) {
      console.error('Session error:', sessionError);
    }
    
    // Check if user is authenticated
    if (session?.user) {
      console.log('✓ User authenticated:', session.user.id);
      
      // Try to access user_profiles table
      const { data: profiles, error: profilesError } = await supabase
        .from('user_profiles')
        .select('*')
        .limit(1);
        
      if (profilesError) {
        console.error('❌ Database access error:', profilesError);
        console.log('This might be due to:');
        console.log('1. Database schema not set up');
        console.log('2. RLS policies blocking access');
        console.log('3. Network connectivity issues');
      } else {
        console.log('✓ Database access successful');
        console.log('Sample profiles:', profiles);
      }
      
      // Check specific user profile
      const { data: userProfile, error: profileError } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', session.user.id)
        .single();
        
      if (profileError) {
        console.log('Profile error:', profileError);
        if (profileError.code === 'PGRST116') {
          console.log('ℹ️ No profile found for user - this is normal for new users');
        }
      } else {
        console.log('✓ User profile found:', userProfile);
      }
      
    } else {
      console.log('ℹ️ No authenticated user');
      
      // Check guest status
      const isGuest = localStorage.getItem('isGuest') === 'true';
      console.log('Guest status:', isGuest);
    }
    
    // Test database connection with a simple query
    const { data: testData, error: testError } = await supabase
      .from('user_profiles')
      .select('count')
      .limit(1);
      
    if (testError) {
      console.error('❌ Database connection test failed:', testError);
    } else {
      console.log('✓ Database connection test successful');
    }
    
  } catch (error) {
    console.error('❌ Debug failed:', error);
  }
};

// Make it available globally for console testing
if (typeof window !== 'undefined') {
  (window as any).debugAuth = debugAuth;
}
