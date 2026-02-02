-- Seed data for development/testing

-- Note: This is for local development only
-- Do not run this in production!

-- Insert test user profile (requires a user to exist in auth.users first)
-- You'll need to sign up through Supabase Auth first, then run this
-- INSERT INTO user_profiles (user_id, subscription_tier)
-- VALUES ('your-user-id-here', 'pro');

-- Example conversation and messages structure
-- (Uncomment and modify after creating a user)

/*
-- Create a sample conversation
INSERT INTO conversations (id, user_id, title, model_provider, model_name)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'your-user-id-here',
    'Welcome Conversation',
    'claude',
    'claude-3-5-sonnet-20241022'
);

-- Add sample messages
INSERT INTO messages (conversation_id, role, content, tokens_used) VALUES
(
    'a0000000-0000-0000-0000-000000000001',
    'user',
    'Hello! Can you help me understand how this AI chat platform works?',
    15
),
(
    'a0000000-0000-0000-0000-000000000001',
    'assistant',
    'Of course! This is a multi-model AI chat platform that allows you to interact with different AI providers (Claude, OpenAI, and Gemini) from a single interface. You can create conversations, switch between models, and track your usage across all providers.',
    65
);

-- Add sample usage record
INSERT INTO usage_records (user_id, conversation_id, provider, model, tokens_used, cost_usd)
VALUES (
    'your-user-id-here',
    'a0000000-0000-0000-0000-000000000001',
    'claude',
    'claude-3-5-sonnet-20241022',
    80,
    0.0024
);
*/
