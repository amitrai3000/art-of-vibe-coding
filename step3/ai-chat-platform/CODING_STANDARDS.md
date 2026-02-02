# Coding Standards - AI Chat Platform

## General Principles

1. **Readability**: Code is read more than written. Optimize for clarity.
2. **Type Safety**: Use TypeScript and Python type hints everywhere.
3. **DRY**: Don't Repeat Yourself. Extract common patterns.
4. **KISS**: Keep It Simple. Avoid over-engineering.
5. **Test**: Write tests for critical business logic.

## TypeScript / JavaScript

### Style Guide

**Formatting**
- Use 2 spaces for indentation
- Single quotes for strings
- Semicolons required
- Max line length: 100 characters

**Naming**
- `camelCase` for variables and functions
- `PascalCase` for components and classes
- `UPPER_SNAKE_CASE` for constants
- `kebab-case` for file names

```typescript
// Good
const userName = 'John';
const MAX_RETRIES = 3;

function fetchUserData() {}

interface UserProfile {}

// Bad
const user_name = 'John';
const maxRetries = 3;
function FetchUserData() {}
```

### React Components

**Component Structure**
```typescript
'use client'; // If client component

import { useState } from 'react';
import { ComponentProps } from '@/types';

interface MyComponentProps {
  title: string;
  onSubmit: (data: string) => void;
  optional?: boolean;
}

export default function MyComponent({
  title,
  onSubmit,
  optional = false
}: MyComponentProps) {
  const [state, setState] = useState('');

  const handleClick = () => {
    // Event handlers
  };

  return (
    <div className="container">
      {/* JSX */}
    </div>
  );
}
```

**Best Practices**
- Always define prop types with TypeScript interfaces
- Extract complex logic into custom hooks
- Use `useCallback` for functions passed as props
- Use `useMemo` for expensive computations
- Prefer functional components over class components
- Keep components under 200 lines (extract if larger)

### Hooks Usage

```typescript
// Good: Extract complex logic
function useUserData(userId: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setData).finally(() => setLoading(false));
  }, [userId]);

  return { data, loading };
}

// Use in component
function UserProfile({ userId }: Props) {
  const { data, loading } = useUserData(userId);
  // ...
}
```

### Async/Await

```typescript
// Good: Explicit error handling
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch:', error);
    throw error;
  }
}

// Bad: Unhandled promise
function fetchData() {
  return fetch('/api/data').then(r => r.json());
}
```

## Python

### Style Guide

**Formatting** (Black + isort)
- 4 spaces for indentation
- Max line length: 100 characters
- Double quotes for strings
- Type hints on all functions

**Naming**
- `snake_case` for variables and functions
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Private methods start with `_`

```python
# Good
user_name = "John"
MAX_RETRIES = 3

def fetch_user_data(user_id: str) -> dict:
    pass

class UserProfile:
    pass

# Bad
userName = "John"
def FetchUserData(userId):
    pass
```

### Type Hints

```python
# Always use type hints
from typing import Dict, List, Optional

def process_message(
    content: str,
    user_id: str,
    metadata: Optional[Dict[str, any]] = None
) -> Dict[str, any]:
    """Process a chat message.

    Args:
        content: Message content
        user_id: User ID
        metadata: Optional metadata

    Returns:
        Processed message dictionary
    """
    # Implementation
    return {"content": content, "user_id": user_id}
```

### Async/Await

```python
# Good: Use async for I/O operations
async def fetch_user(user_id: str) -> dict:
    """Fetch user from database."""
    supabase = get_supabase_client()
    response = await supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data

# Bad: Blocking I/O
def fetch_user(user_id: str) -> dict:
    response = requests.get(f"/users/{user_id}")
    return response.json()
```

### Error Handling

```python
# Good: Specific exceptions, proper logging
import logging

logger = logging.getLogger(__name__)

async def process_chat(message: str) -> str:
    try:
        response = await ai_provider.generate(message)
        return response.content
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise

# Bad: Bare except, no logging
def process_chat(message):
    try:
        return ai_provider.generate(message)
    except:
        return "Error"
```

### FastAPI Routes

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import ChatRequest, ChatResponse
from app.dependencies import get_current_user_id

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def create_chat(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
) -> ChatResponse:
    """Create a chat completion.

    Args:
        request: Chat request parameters
        user_id: Current user ID from JWT

    Returns:
        Chat response with completion
    """
    # Implementation
    pass
```

## Database

### Supabase Queries

```typescript
// Good: Typed queries with error handling
const { data, error } = await supabase
  .from('conversations')
  .select('*')
  .eq('user_id', userId)
  .order('updated_at', { ascending: false });

if (error) {
  console.error('Query failed:', error);
  throw new Error('Failed to fetch conversations');
}

return data;

// Bad: No error handling
const data = await supabase
  .from('conversations')
  .select('*')
  .eq('user_id', userId);
return data;
```

### Migrations

```sql
-- Always include:
-- 1. Comments explaining purpose
-- 2. Indexes for performance
-- 3. RLS policies for security

-- Create table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Enable RLS
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Add policies
CREATE POLICY "Users can view own conversations"
    ON conversations FOR SELECT
    USING (auth.uid() = user_id);
```

## API Design

### REST Endpoints

```
GET    /api/v1/conversations        # List user's conversations
POST   /api/v1/conversations        # Create conversation
GET    /api/v1/conversations/:id    # Get conversation
PUT    /api/v1/conversations/:id    # Update conversation
DELETE /api/v1/conversations/:id    # Delete conversation

POST   /api/v1/chat                 # Create chat completion
```

### Request/Response Format

```typescript
// Request
interface ChatRequest {
  conversation_id?: string;
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  provider: 'claude' | 'openai' | 'gemini';
  stream?: boolean;
}

// Response
interface ChatResponse {
  conversation_id: string;
  message_id: string;
  content: string;
  tokens_used: number;
}

// Error
interface ErrorResponse {
  detail: string;
  code?: string;
}
```

## Testing

### Backend Tests (pytest)

```python
import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_chat_completion(client: TestClient, mock_user_id: str):
    """Test chat completion endpoint."""
    response = client.post(
        "/api/v1/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "provider": "claude",
        },
        headers={"Authorization": f"Bearer {mock_jwt_token}"},
    )
    assert response.status_code == 200
```

### Frontend Tests (Jest)

```typescript
import { render, screen } from '@testing-library/react';
import MessageList from '@/components/chat/MessageList';

describe('MessageList', () => {
  it('renders messages correctly', () => {
    const messages = [
      { id: '1', role: 'user', content: 'Hello', created_at: new Date() },
      { id: '2', role: 'assistant', content: 'Hi!', created_at: new Date() },
    ];

    render(<MessageList messages={messages} />);

    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('Hi!')).toBeInTheDocument();
  });
});
```

## Git Commit Messages

```
feat: Add streaming support for Gemini provider
fix: Handle null conversation_id in chat endpoint
docs: Update API documentation for quota endpoints
refactor: Extract AI provider factory to separate module
test: Add integration tests for usage tracking
chore: Update dependencies to latest versions
```

Format: `type: description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Add/update tests
- `chore`: Maintenance tasks

## Security

### Never Commit Secrets

```typescript
// Bad: Hardcoded secrets
const apiKey = 'sk-ant-1234567890';

// Good: Environment variables
const apiKey = process.env.ANTHROPIC_API_KEY;
```

### Validate All Inputs

```python
# Good: Use Pydantic for validation
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    provider: str = Field(..., regex="^(claude|openai|gemini)$")

# Bad: No validation
def chat(content, provider):
    # Direct use of user input
    pass
```

### SQL Injection Prevention

```typescript
// Good: Parameterized queries (Supabase does this)
await supabase
  .from('users')
  .select()
  .eq('email', userEmail);

// Bad: String concatenation
await supabase.rpc('raw_query', {
  query: `SELECT * FROM users WHERE email = '${userEmail}'`
});
```

## Performance

### Database Queries

```typescript
// Good: Single query with joins
const { data } = await supabase
  .from('conversations')
  .select('*, messages(*)')
  .eq('user_id', userId);

// Bad: N+1 queries
const conversations = await supabase.from('conversations').select();
for (const conv of conversations) {
  const messages = await supabase
    .from('messages')
    .select()
    .eq('conversation_id', conv.id);
}
```

### React Rendering

```typescript
// Good: Memoize expensive computations
const sortedMessages = useMemo(
  () => messages.sort((a, b) => a.created_at - b.created_at),
  [messages]
);

// Bad: Sort on every render
function MessageList({ messages }) {
  const sorted = messages.sort((a, b) => a.created_at - b.created_at);
  // ...
}
```

## Documentation

### Code Comments

```python
# Good: Explain WHY, not WHAT
# Use service role key here because we need to bypass RLS
# to access usage records across all users for aggregation
supabase = create_client(url, service_role_key)

# Bad: Stating the obvious
# Create supabase client
supabase = create_client(url, service_role_key)
```

### Function Documentation

Always include:
- Purpose of the function
- Parameters and their types
- Return value
- Exceptions that may be raised

```python
async def check_quota(user_id: str) -> Dict[str, any]:
    """Check if user has quota available.

    Args:
        user_id: User ID to check quota for

    Returns:
        Dictionary with quota information:
        - tokens_used: Current month usage
        - tokens_remaining: Remaining quota
        - has_quota: Boolean indicating availability

    Raises:
        ValueError: If user_id is invalid
    """
    pass
```

## Code Review Checklist

- [ ] Code follows style guide (formatting, naming)
- [ ] All functions have type hints / TypeScript types
- [ ] Error handling is comprehensive
- [ ] No secrets hardcoded
- [ ] Tests added for new features
- [ ] Documentation updated
- [ ] Performance considerations addressed
- [ ] Security implications considered
