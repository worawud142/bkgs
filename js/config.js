// Supabase Configuration
// Get your actual keys from: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/api
const SUPABASE_URL = 'https://qceqiasyoufutqnsbbjp.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjZXFpYXN5b3VmdXRxbnNiYmpwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjgxOTA3OTMsImV4cCI6MjA4Mzc2Njc5M30.FjlgPXNDvSFjh88_DxETXaW80ghhbfUhkx3q5n9g3qA';

// Initialize Supabase Client
// Use a different variable name to avoid conflict with the Supabase library
let supabaseClient = null;

try {
    if (typeof window.supabase !== 'undefined' && typeof window.supabase.createClient === 'function') {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log('✅ Supabase initialized successfully');
    } else {
        console.error('❌ Supabase library not loaded');
    }
} catch (error) {
    console.error('❌ Error initializing Supabase:', error);
}

// Export as global variable for use in other scripts
window.supabase = supabaseClient;
