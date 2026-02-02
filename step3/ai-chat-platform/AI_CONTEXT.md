# AI Context - AI Chat Platform

This document provides context for AI assistants working on this project.

## Project Overview

**Name**: AI Chat Platform
**Type**: SaaS Multi-Model AI Chat Application
**Architecture**: Hybrid (Next.js Frontend + Python FastAPI Backend)
**Target Users**: B2B developers and technical teams
**Scale**: 1K-10K users in first year
**Monetization**: Freemium with usage-based paid tiers

## Core Purpose

Provide a unified interface for developers to interact with multiple AI models (Claude, OpenAI, Gemini) from a single platform, with conversation history, usage tracking, and team collaboration features.

## Technology Decisions

### Frontend (Next.js)
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS with custom design tokens
- **State**: Zustand for global state management
- **Auth**: Supabase Auth with OAuth (Google, GitHub)
- **Deployment**: Vercel

**Rationale**: Next.js provides excellent DX, SSR capabilities, and seamless Vercel deployment. TypeScript ensures type safety across the codebase.

### Backend (Python FastAPI)
- **Framework**: FastAPI with async/await
- **Language**: Python 3.12+ with type hints
- **AI SDKs**: Anthropic, OpenAI, Google Generative AI
- **Jobs**: Celery + Redis for background tasks
- **Deployment**: Docker containers on Fly.io/Railway

**Rationale**: Python has first-class AI SDK support. FastAPI provides async streaming for real-time responses. Celery handles usage aggregation and billing tasks.

### Database & Infrastructure
- **Database**: Supabase (Managed PostgreSQL)
- **Auth**: Supabase Auth
- **Cache/Queue**: Redis (Upstash for serverless)
- **Storage**: Supabase Storage
- **Payments**: Stripe

**Rationale**: Supabase provides managed database, auth, and realtime out of the box. Redis handles caching and Celery job queue.

## Architecture Patterns

### Service Communication
- Frontend → Next.js API Routes → Python Backend → AI Providers
- JWT tokens from Supabase Auth for authentication
- Server-Sent Events (SSE) for streaming AI responses

### Data Flow
1. User authenticates via Supabase Auth (OAuth)
2. User sends message through Next.js UI
3. Next.js API route validates auth and forwards to Python backend
4. Python backend checks quota, calls AI provider, streams response
5. Backend records usage in Supabase
6. Celery workers aggregate usage hourly

### Background Jobs (Celery)
- **Hourly**: Aggregate usage statistics
- **Daily**: Check quota warnings, send notification emails
- **Monthly**: Generate Stripe invoices for usage-based billing

## Code Organization

### Frontend Structure
```
frontend/src/
├── app/              # Next.js pages (App Router)
├── components/       # Reusable React components
├── lib/              # Utilities, clients (Supabase, Stripe)
├── store/            # Zustand state stores
└── types/            # TypeScript type definitions
```

### Backend Structure
```
backend/app/
├── api/v1/           # FastAPI route handlers
├── services/ai/      # AI provider implementations (Claude, OpenAI, Gemini)
├── workers/          # Celery tasks and configuration
├── models/           # Pydantic schemas
├── db/               # Database clients and utilities
└── middleware/       # Error handling, auth verification
```

## Key Design Patterns

### AI Provider Abstraction
- **Base Class**: `BaseAIProvider` defines interface
- **Implementations**: `ClaudeProvider`, `OpenAIProvider`, `GeminiProvider`
- **Factory**: `AIProviderFactory` creates instances based on user selection
- **Streaming**: Unified async generator interface for all providers

### Authentication Flow
- Supabase Auth handles OAuth
- JWT tokens stored in HTTP-only cookies
- Backend verifies JWT using Supabase public key
- Row Level Security (RLS) in database ensures data isolation

### Error Handling
- FastAPI middleware catches all exceptions
- Structured JSON error responses
- Sentry integration for production error tracking
- Graceful degradation (e.g., quota checks fail open)

## Development Conventions

### TypeScript
- Strict mode enabled
- Explicit types for all function parameters and returns
- Use interfaces for data structures
- Prefer functional components with hooks

### Python
- Type hints on all functions
- Async/await for I/O operations
- Pydantic for data validation
- Black + isort for formatting
- Ruff for linting

### Git Workflow
- Feature branches from `main`
- Descriptive commit messages
- PR reviews required
- CI runs tests and linting

### Environment Variables
- Never commit `.env` files
- Use `.env.example` as template
- Validate required vars on startup
- Use `pydantic-settings` (Python) and Next.js env validation

## Testing Strategy

### Backend
- `pytest` for unit and integration tests
- Mock Supabase and AI provider calls
- Test quota enforcement logic
- Test streaming response handling

### Frontend
- Jest for unit tests
- React Testing Library for component tests
- E2E tests with Playwright (future)

## Security Considerations

- **Auth**: JWT verification on all protected endpoints
- **RLS**: Supabase Row Level Security ensures users only access their data
- **Input Validation**: Pydantic schemas validate all API inputs
- **Rate Limiting**: Implement rate limits on chat endpoints
- **Secrets**: Use environment variables, never hardcode
- **CORS**: Restrict to known frontend origins

## Performance Optimizations

- **Streaming**: Use SSE for real-time AI responses (better UX than polling)
- **Caching**: Redis caches frequently accessed data
- **Database**: Indexes on user_id, conversation_id, created_at
- **Frontend**: Code splitting, lazy loading components
- **CDN**: Static assets served via Vercel Edge Network

## Common Gotchas

### Supabase RLS
- Service role key bypasses RLS (use for backend operations)
- Anon key enforces RLS (use for frontend)
- Always test RLS policies with actual user tokens

### Celery
- Tasks must be idempotent (can run multiple times safely)
- Use `task_acks_late=True` for reliability
- Monitor queue depth to avoid backlog

### Streaming Responses
- Keep connections alive with periodic heartbeat
- Handle client disconnections gracefully
- Buffer small chunks to reduce overhead

### TypeScript + Next.js
- Server components can't use hooks or browser APIs
- Client components need 'use client' directive
- API routes run server-side, have access to secrets

## Deployment Checklist

- [ ] Set all environment variables in deployment platform
- [ ] Run database migrations in Supabase
- [ ] Configure OAuth redirect URLs
- [ ] Set up Stripe webhooks
- [ ] Enable Sentry for error tracking
- [ ] Configure CORS origins
- [ ] Test authentication flow
- [ ] Test AI provider integrations
- [ ] Verify background jobs are running
- [ ] Set up monitoring and alerts

## Future Enhancements

### Phase 2 (3-6 months)
- File upload and document processing
- RAG integration with vector search
- Team collaboration features
- Advanced analytics dashboard

### Phase 3 (6-12 months)
- Mobile app (React Native)
- API access for developers
- Custom model fine-tuning
- Enterprise SSO support

## Resources

- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs
- **Anthropic API**: https://docs.anthropic.com
- **OpenAI API**: https://platform.openai.com/docs
- **Celery Docs**: https://docs.celeryproject.org

## When Working on This Project

1. **Read CODING_STANDARDS.md** for style guidelines
2. **Check PLAN.md** for current priorities
3. **Use sub-agents** in `.claude/agents/` for specialized tasks
4. **Follow templates** in `templates/` for new features
5. **Update this document** when architecture changes

## Quick Commands

```bash
# Start everything
docker compose up

# Backend only
cd backend && uvicorn app.main:app --reload

# Frontend only
cd frontend && npm run dev

# Run tests
cd backend && pytest
cd frontend && npm run type-check

# Format code
cd backend && black . && isort .
cd frontend && npm run lint
```
