# AI Chat Platform - Frontend

Next.js frontend for multi-model AI chat platform.

## Features

- **Multi-Model Support**: Switch between Claude, OpenAI, and Gemini
- **Real-time Streaming**: Server-Sent Events for live responses
- **Conversation Management**: Create, view, and manage chat history
- **Authentication**: Supabase Auth with OAuth
- **Responsive UI**: Tailwind CSS with clean chat interface

## Tech Stack

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Supabase (auth, database, realtime)
- Zustand (state management)
- Vercel AI SDK

## Setup

### Prerequisites

- Node.js 18.17+
- Supabase project
- Backend service running

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
```

### Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_APP_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=your_stripe_key
```

## Development

```bash
# Run development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Type check
npm run type-check

# Lint
npm run lint

# Production build
npm run build

# Start production server
npm start
```

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── page.tsx        # Home page
│   ├── chat/[id]/      # Chat page
│   └── api/            # API routes
├── components/
│   ├── chat/           # Chat components
│   ├── layout/         # Layout components
│   └── auth/           # Auth components
├── lib/
│   ├── supabase/       # Supabase clients
│   ├── utils.ts        # Utilities
│   └── stripe.ts       # Stripe client
├── store/
│   └── chat.ts         # Zustand store
└── types/
    └── index.ts        # TypeScript types
```

## Key Features

### Authentication Flow

1. User signs in via Supabase Auth (OAuth)
2. JWT token stored in cookies
3. Token sent to backend for API requests

### Chat Flow

1. User types message in MessageInput
2. Message sent to Next.js API route
3. API route forwards to Python backend with auth token
4. Backend streams response via SSE
5. Frontend updates UI in real-time

### State Management

Using Zustand for:
- Current conversation
- Message history
- Selected AI provider
- Loading states

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### Environment Variables for Production

Set these in Vercel dashboard:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_APP_URL`
- `BACKEND_URL`
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

## Supabase Setup

1. Create project at supabase.com
2. Enable OAuth providers (Google, GitHub)
3. Run database migrations
4. Copy keys to `.env.local`

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
