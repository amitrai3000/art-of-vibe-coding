# AI Chat Platform - Backend

FastAPI backend service for multi-model AI chat platform.

## Features

- **Multi-Model AI Support**: Claude, OpenAI, Gemini
- **Streaming Responses**: Real-time SSE streaming
- **Usage Tracking**: Token counting and cost tracking
- **Quota Enforcement**: Tier-based limits
- **Background Jobs**: Celery workers for async tasks
- **Authentication**: JWT verification from Supabase

## Tech Stack

- FastAPI (async Python web framework)
- Supabase (database, auth)
- Redis (caching, Celery broker)
- Celery (background jobs)
- Anthropic, OpenAI, Google AI SDKs

## Setup

### Prerequisites

- Python 3.12+
- Redis (for Celery)
- Supabase project

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
# Required
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret
BACKEND_SECRET_KEY=generate_a_random_key

# AI Providers (at least one required)
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Redis
REDIS_URL=redis://localhost:6379/0
```

## Development

### Run Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Celery Worker

```bash
# Start worker
celery -A app.workers.celery_app worker --loglevel=info

# Start beat scheduler
celery -A app.workers.celery_app beat --loglevel=info
```

### Run Tests

```bash
pytest
pytest --cov=app tests/  # With coverage
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint
ruff check .

# Type checking
mypy app/
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── main.py              # FastAPI application
├── config.py            # Configuration
├── dependencies.py      # Dependency injection
├── api/
│   └── v1/              # API routes
├── services/
│   ├── ai/              # AI provider implementations
│   ├── usage.py         # Usage tracking
│   └── quota.py         # Quota enforcement
├── models/
│   └── schemas.py       # Pydantic models
├── db/
│   └── supabase.py      # Database client
├── workers/
│   ├── celery_app.py    # Celery config
│   └── tasks.py         # Background tasks
└── middleware/
    └── error_handler.py # Error handling
```

## Docker

```bash
# Build image
docker build -t ai-chat-backend .

# Run container
docker run -p 8000:8000 --env-file .env ai-chat-backend
```

## Production Deployment

See main README for deployment instructions to Fly.io or Railway.
