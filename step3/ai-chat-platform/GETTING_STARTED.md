# Getting Started with AI Chat Platform

Welcome! This guide will help you get the AI Chat Platform running on your local machine in under 10 minutes.

## Prerequisites

Before you begin, ensure you have:

- [x] **Node.js 18.17+** - [Download](https://nodejs.org/)
- [x] **Python 3.12+** - [Download](https://python.org/)
- [x] **Docker Desktop** - [Download](https://docker.com/products/docker-desktop)
- [x] **Supabase Account** - [Sign up](https://supabase.com/)
- [x] **At least one AI API key**:
  - Anthropic (Claude): [Get API key](https://console.anthropic.com/)
  - OpenAI: [Get API key](https://platform.openai.com/)
  - Google AI: [Get API key](https://makersuite.google.com/)

## Quick Start (Docker - Recommended)

### 1. Clone and Configure

```bash
cd ai-chat-platform
cp .env.example .env
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Once created, get your credentials from Settings > API:
   - Project URL
   - Anon (public) key
   - Service role key
3. Get your JWT secret from Settings > API > JWT Settings

### 3. Edit .env File

Open `.env` and add your credentials:

```bash
# Supabase (REQUIRED)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here

# AI Provider (at least one REQUIRED)
ANTHROPIC_API_KEY=sk-ant-xxxxx
# OR
OPENAI_API_KEY=sk-xxxxx
# OR
GOOGLE_API_KEY=xxxxx

# Leave these as-is for local development
NEXT_PUBLIC_APP_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_chat_platform
REDIS_URL=redis://localhost:6379/0
BACKEND_SECRET_KEY=dev-secret-change-in-production
BACKEND_CORS_ORIGINS=http://localhost:3000
```

### 4. Set Up Database

In Supabase dashboard:
1. Go to SQL Editor
2. Open `supabase/migrations/001_initial_schema.sql` from this project
3. Copy the entire contents
4. Paste into Supabase SQL Editor
5. Click "Run"

### 5. Enable OAuth (Optional but Recommended)

In Supabase dashboard:
1. Go to Authentication > Providers
2. Enable Google and/or GitHub
3. Add OAuth credentials from [Google Console](https://console.cloud.google.com/) or [GitHub Settings](https://github.com/settings/developers)
4. Add authorized redirect URL: `https://your-project.supabase.co/auth/v1/callback`

### 6. Start Everything!

```bash
docker compose up
```

Wait for all services to start (30-60 seconds). You'll see:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 7. Test It Out

1. Open http://localhost:3000
2. Click "Sign In"
3. Authenticate with Google or GitHub
4. Create a new conversation
5. Select an AI model
6. Start chatting!

## Manual Setup (Without Docker)

If you prefer not to use Docker:

### Terminal 1: Database & Redis

```bash
# Start PostgreSQL (or use existing instance)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:16

# Start Redis
docker run -d -p 6379:6379 redis:7
```

### Terminal 2: Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3: Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Terminal 4: Celery Worker (Optional)

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start worker
celery -A app.workers.celery_app worker --loglevel=info
```

### Terminal 5: Celery Beat (Optional)

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start scheduler
celery -A app.workers.celery_app beat --loglevel=info
```

## Troubleshooting

### "Cannot connect to Supabase"
- Verify your Supabase URL and keys in `.env`
- Check that database migration ran successfully
- Ensure Supabase project is active

### "AI provider error"
- Verify API keys are correct
- Check that you have credits/quota with the AI provider
- Try a different provider

### "Port already in use"
- Frontend (3000): Stop other Next.js apps
- Backend (8000): Stop other FastAPI apps
- Postgres (5432): Stop other PostgreSQL instances
- Redis (6379): Stop other Redis instances

### "Module not found" errors
- Backend: Ensure virtual environment is activated and dependencies installed
- Frontend: Run `npm install` in frontend directory

### Docker issues
- Run `docker compose down -v` to clean up
- Run `docker compose up --build` to rebuild
- Check Docker Desktop is running

## Next Steps

Once you have the platform running:

1. **Read the Documentation**
   - `README.md` - Project overview
   - `AI_CONTEXT.md` - Architecture and patterns
   - `CODING_STANDARDS.md` - Code style guide
   - `PLAN.md` - Development roadmap

2. **Explore the Codebase**
   - Frontend: `frontend/src/`
   - Backend: `backend/app/`
   - Database: `supabase/migrations/`

3. **Start Developing**
   - Check `PLAN.md` for current priorities
   - Use templates in `templates/` for new features
   - Consult sub-agents in `.claude/agents/` for specialized help

4. **Run Tests**
   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend
   npm run type-check
   npm run lint
   ```

## Common Commands

```bash
# Start all services
docker compose up

# Stop all services
docker compose down

# Rebuild after code changes
docker compose up --build

# View logs
docker compose logs -f

# Backend only
cd backend && uvicorn app.main:app --reload

# Frontend only
cd frontend && npm run dev

# Run backend tests
cd backend && pytest

# Format backend code
cd backend && black . && isort .

# Type check frontend
cd frontend && npm run type-check
```

## Getting Help

- **Bug Reports**: Open an issue on GitHub
- **Questions**: Check `AI_CONTEXT.md` or ask in discussions
- **Code Style**: See `CODING_STANDARDS.md`
- **Architecture**: See `AI_CONTEXT.md`

## What's Included

- Multi-model AI chat (Claude, OpenAI, Gemini)
- Real-time streaming responses
- User authentication (OAuth)
- Conversation history
- Usage tracking
- Background job processing
- Docker development environment
- CI/CD pipelines
- Comprehensive documentation

## Project Structure

```
ai-chat-platform/
├── frontend/           # Next.js app
├── backend/            # FastAPI service
├── supabase/           # Database migrations
├── .claude/agents/     # Development helpers
├── templates/          # Feature templates
├── .github/workflows/  # CI/CD
└── docker-compose.yml  # Local environment
```

## License

MIT - See LICENSE file

## Support

For detailed documentation, see the main `README.md` file.

Happy coding!
