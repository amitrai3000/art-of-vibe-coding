"""Pydantic models for request/response validation."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AIProvider(str, Enum):
    """Supported AI providers."""

    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"


class MessageRole(str, Enum):
    """Message roles in a conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Chat message schema."""

    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    """Request schema for chat completion."""

    conversation_id: Optional[str] = None
    messages: List[ChatMessage]
    provider: AIProvider = Field(default=AIProvider.CLAUDE)
    model: Optional[str] = None
    stream: bool = Field(default=True)
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=4096)


class ChatResponse(BaseModel):
    """Response schema for chat completion."""

    conversation_id: str
    message_id: str
    content: str
    provider: AIProvider
    model: str
    tokens_used: int
    finish_reason: Optional[str] = None


class ConversationCreate(BaseModel):
    """Schema for creating a new conversation."""

    title: Optional[str] = Field(default="New Conversation")
    model_provider: AIProvider = Field(default=AIProvider.CLAUDE)
    model_name: str


class ConversationResponse(BaseModel):
    """Response schema for conversation."""

    id: str
    user_id: str
    title: str
    model_provider: str
    model_name: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    """Response schema for a message."""

    id: str
    conversation_id: str
    role: str
    content: str
    tokens_used: Optional[int] = None
    created_at: datetime


class UsageStats(BaseModel):
    """Usage statistics for a user."""

    total_messages: int
    total_tokens: int
    total_cost_usd: float
    by_provider: Dict[str, Any]


class QuotaInfo(BaseModel):
    """User quota information."""

    tier: str
    tokens_limit: int
    tokens_used: int
    tokens_remaining: int
    reset_date: Optional[datetime] = None


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str
    code: Optional[str] = None
