# Supabase Database

This directory contains database migrations and setup for the AI Chat Platform.

## Setup

### Using Supabase Cloud

1. Create a new project at [supabase.com](https://supabase.com)
2. Copy your project URL and keys to `.env`
3. Run the migration SQL in Supabase SQL Editor:
   - Navigate to SQL Editor in Supabase dashboard
   - Paste contents of `migrations/001_initial_schema.sql`
   - Run the migration

### Using Local Supabase

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase
supabase init

# Start local Supabase
supabase start

# Apply migrations
supabase db push

# (Optional) Seed data
supabase db seed
```

## Migrations

Migrations are in `migrations/` directory and numbered sequentially:
- `001_initial_schema.sql` - Initial database schema

## Schema Overview

### Tables

**user_profiles**
- Extends Supabase auth.users
- Stores subscription tier and Stripe customer ID

**conversations**
- User's chat conversations
- Tracks model provider and model name

**messages**
- Individual messages in conversations
- Stores role (user/assistant), content, token usage

**usage_records**
- Detailed usage tracking
- Per-message token usage and cost

### RLS Policies

All tables have Row Level Security enabled:
- Users can only access their own data
- Service role key bypasses RLS for backend operations

### Functions

**get_monthly_usage(user_id)**
- Returns total tokens used this month for a user

**get_users_near_quota()**
- Returns users at 80%+ of their quota
- Used by Celery worker for warning emails

## Adding Migrations

Create new migration files:

```sql
-- migrations/002_add_feature.sql
-- Your schema changes here
```

Apply with Supabase CLI:
```bash
supabase db push
```

Or run manually in Supabase SQL Editor.
