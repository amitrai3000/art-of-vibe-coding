export type AIProvider = 'claude' | 'openai' | 'gemini';

export type MessageRole = 'user' | 'assistant' | 'system';

export interface Message {
  id: string;
  conversation_id: string;
  role: MessageRole;
  content: string;
  tokens_used?: number;
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  model_provider: AIProvider;
  model_name: string;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  conversation_id?: string;
  messages: Array<{
    role: MessageRole;
    content: string;
  }>;
  provider: AIProvider;
  model?: string;
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
}

export interface UsageStats {
  total_messages: number;
  total_tokens: number;
  total_cost_usd: number;
  by_provider: Record<string, {
    tokens: number;
    cost: number;
    requests: number;
  }>;
}

export interface QuotaInfo {
  tier: string;
  tokens_limit: number;
  tokens_used: number;
  tokens_remaining: number;
  reset_date?: string;
}

export interface UserProfile {
  id: string;
  user_id: string;
  subscription_tier: 'free' | 'pro' | 'enterprise';
  stripe_customer_id?: string;
  created_at: string;
  updated_at: string;
}
