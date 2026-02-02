# AI Chat Platform

A production-ready, multi-model AI chat platform that allows users to interact with Claude, OpenAI, and Gemini from a single interface.

## Overview

This platform provides a seamless chat experience across multiple AI providers with:
- Real-time streaming responses
- Conversation history and management
- Usage tracking and quota enforcement
- Subscription-based billing
- OAuth authentication
- Background job processing

## Architecture

**Pattern**: Hybrid Next.js + Python AI Service

```
Frontend (Next.js) → Backend (FastAPI) → AI Providers
      ↓                    ↓
   Supabase          Celery Workers
```

### Tech Stack

**Frontend**
- Next.js 14+ (App Router, TypeScript)
- Tailwind CSS
- Supabase Auth
- Zustand state management

**Backend**
- Python 3.12+ with FastAPI
- Anthropic, OpenAI, Google AI SDKs
- Celery + Redis for background jobs
- Supabase for database

**Infrastructure**
- Supabase (Postgres, Auth, Storage, Realtime)
- Redis (caching, job queue)
- Docker for local development

## Quick Start

### Prerequisites

- Node.js 18.17+
- Python 3.12+
- Docker and Docker Compose
- Supabase account
- API keys (at least one): Anthropic, OpenAI, or Google

### 1. Clone and Setup

```bash
cd ai-chat-platform
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your credentials:

```bash
# Supabase (from supabase.com dashboard)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret

# AI Provider Keys (at least one required)
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
GOOGLE_API_KEY=xxx

# Stripe (optional for billing)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx

# Email (optional)
RESEND_API_KEY=re_xxx
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Set Up Supabase Database

1. Go to [supabase.com](https://supabase.com) and create a project
2. In SQL Editor, run the migration:
   ```sql
   -- Copy contents of supabase/migrations/001_initial_schema.sql
   ```
3. Enable OAuth providers in Authentication settings (Google, GitHub)

### 4. Start with Docker Compose

```bash
# Start all services
docker compose up

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Postgres: localhost:5432
# - Redis: localhost:6379
```

### 5. Manual Setup (Alternative)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Celery Worker:**
```bash
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

**Celery Beat:**
```bash
cd backend
celery -A app.workers.celery_app beat --loglevel=info
```

## Usage

1. Navigate to http://localhost:3000
2. Click "Sign In" and authenticate with Google or GitHub
3. Create a new conversation
4. Select an AI provider (Claude, OpenAI, or Gemini)
5. Start chatting!

## Project Structure

```
ai-chat-platform/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages & API routes
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities, Supabase client
│   │   ├── store/           # Zustand state
│   │   └── types/           # TypeScript types
│   └── package.json
│
├── backend/                  # FastAPI service
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── services/ai/     # AI provider implementations
│   │   ├── workers/         # Celery tasks
│   │   ├── models/          # Pydantic schemas
│   │   └── main.py          # FastAPI app
│   └── requirements.txt
│
├── supabase/                 # Database migrations
│   └── migrations/
│
├── .claude/agents/           # Claude Code sub-agents
├── templates/                # Development templates
├── .github/workflows/        # CI/CD pipelines
├── docker-compose.yml
└── README.md
```

## Development

### Running Tests

**Backend:**
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
```

**Frontend:**
```bash
cd frontend
npm run type-check
npm run lint
```

### Code Quality

**Backend:**
```bash
cd backend
black .              # Format
isort .              # Sort imports
ruff check .         # Lint
mypy app/            # Type check
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Database Migrations

```bash
# Using Supabase CLI
supabase db push

# Or manually run SQL in Supabase SQL Editor
```

## Features

### Implemented
- Multi-model AI chat (Claude, OpenAI, Gemini)
- Real-time streaming responses
- Conversation management
- OAuth authentication
- Usage tracking
- Quota enforcement by tier
- Background job processing
- Celery workers for async tasks

### Roadmap
- File upload and processing
- Team collaboration features
- Advanced analytics dashboard
- Custom model fine-tuning
- API access for developers
- Mobile app (React Native)

## Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel
```

Set environment variables in Vercel dashboard.

### Backend (Fly.io)

```bash
cd backend
fly launch
fly deploy
```

### Backend (Railway)

1. Connect GitHub repo to Railway
2. Add environment variables
3. Deploy backend service

See `DEPLOYMENT.md` for detailed instructions.

## API Documentation

Once running, visit:
- Backend API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Contributing

See `CODING_STANDARDS.md` for code style and conventions.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check `AI_CONTEXT.md` for project context
- Review component README files
- Open an issue on GitHub

## Security

- Never commit `.env` files
- Rotate API keys regularly
- Use Row Level Security (RLS) in Supabase
- Validate all user inputs
- Rate limit API endpoints

## Monitoring

The platform includes:
- Sentry for error tracking
- Vercel Analytics for frontend metrics
- Structured logging with OpenTelemetry
- Usage and cost tracking

## Cost Estimates

For 1K-10K users:
- Infrastructure: ~$110-130/month
- AI API costs: Variable (usage-based)
- Stripe fees: 2.9% + $0.30 per transaction

See architecture docs for detailed breakdown.
