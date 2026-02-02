// This file will be auto-generated from Supabase CLI in production
// For now, using a placeholder type

export type Database = {
  public: {
    Tables: {
      user_profiles: {
        Row: {
          id: string;
          user_id: string;
          subscription_tier: string;
          stripe_customer_id: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          user_id: string;
          subscription_tier?: string;
          stripe_customer_id?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          user_id?: string;
          subscription_tier?: string;
          stripe_customer_id?: string | null;
          created_at?: string;
          updated_at?: string;
        };
      };
      conversations: {
        Row: {
          id: string;
          user_id: string;
          title: string;
          model_provider: string;
          model_name: string;
          created_at: string;
          updated_at: string;
        };
      };
      messages: {
        Row: {
          id: string;
          conversation_id: string;
          role: string;
          content: string;
          tokens_used: number | null;
          created_at: string;
        };
      };
      usage_records: {
        Row: {
          id: string;
          user_id: string;
          conversation_id: string | null;
          provider: string;
          model: string;
          tokens_used: number;
          cost_usd: number;
          created_at: string;
        };
      };
    };
  };
};
