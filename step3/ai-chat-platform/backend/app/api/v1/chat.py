"""Chat endpoints."""

import json
import logging
import uuid
from datetime import datetime
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.dependencies import get_current_user_id
from app.db.supabase import get_supabase_client
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    MessageRole,
)
from app.services.ai.factory import AIProviderFactory
from app.services.quota import QuotaService
from app.services.usage import UsageService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=None)
async def create_chat_completion(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Create a chat completion.

    Args:
        request: Chat request parameters
        user_id: Current user ID from JWT token

    Returns:
        Chat response (streaming or non-streaming)

    Raises:
        HTTPException: If quota is exceeded or provider fails
    """
    try:
        # Check quota
        quota_service = QuotaService()
        await quota_service.enforce_quota(user_id)

        # Create AI provider
        provider = AIProviderFactory.create_provider(
            provider=request.provider,
            model=request.model,
        )

        # Get or create conversation
        supabase = get_supabase_client()
        conversation_id = request.conversation_id

        if not conversation_id:
            # Create new conversation
            conversation = (
                supabase.table("conversations")
                .insert(
                    {
                        "user_id": user_id,
                        "title": "New Conversation",
                        "model_provider": request.provider.value,
                        "model_name": provider.model,
                    }
                )
                .execute()
            )
            conversation_id = conversation.data[0]["id"]

        # Save user message
        user_message = (
            supabase.table("messages")
            .insert(
                {
                    "conversation_id": conversation_id,
                    "role": MessageRole.USER.value,
                    "content": request.messages[-1].content,
                }
            )
            .execute()
        )

        if request.stream:
            # Return streaming response
            return StreamingResponse(
                stream_chat_response(
                    provider=provider,
                    request=request,
                    conversation_id=conversation_id,
                    user_id=user_id,
                ),
                media_type="text/event-stream",
            )
        else:
            # Generate non-streaming response
            response = await provider.generate_response(
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            # Save assistant message
            assistant_message = (
                supabase.table("messages")
                .insert(
                    {
                        "conversation_id": conversation_id,
                        "role": MessageRole.ASSISTANT.value,
                        "content": response["content"],
                        "tokens_used": response["tokens_used"],
                    }
                )
                .execute()
            )

            # Record usage
            usage_service = UsageService()
            await usage_service.record_usage(
                user_id=user_id,
                conversation_id=conversation_id,
                provider=request.provider.value,
                model=provider.model,
                tokens_used=response["tokens_used"],
            )

            return ChatResponse(
                conversation_id=conversation_id,
                message_id=assistant_message.data[0]["id"],
                content=response["content"],
                provider=request.provider,
                model=provider.model,
                tokens_used=response["tokens_used"],
                finish_reason=response["finish_reason"],
            )

    except ValueError as e:
        logger.error(f"Chat ValueError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate chat completion: {str(e)}",
        )


async def stream_chat_response(
    provider,
    request: ChatRequest,
    conversation_id: str,
    user_id: str,
) -> AsyncGenerator[str, None]:
    """Stream chat response in Server-Sent Events format.

    Args:
        provider: AI provider instance
        request: Chat request
        conversation_id: Conversation ID
        user_id: User ID

    Yields:
        Server-Sent Events formatted messages
    """
    full_content = ""
    tokens_used = 0

    try:
        # Stream response chunks
        async for chunk in provider.stream_response(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        ):
            full_content += chunk
            yield f"data: {json.dumps({'content': chunk})}\n\n"

        # Estimate tokens (will be more accurate with proper tokenizer)
        tokens_used = provider.count_tokens(full_content)

        # Save assistant message
        supabase = get_supabase_client()
        assistant_message = (
            supabase.table("messages")
            .insert(
                {
                    "conversation_id": conversation_id,
                    "role": MessageRole.ASSISTANT.value,
                    "content": full_content,
                    "tokens_used": tokens_used,
                }
            )
            .execute()
        )

        # Record usage
        usage_service = UsageService()
        await usage_service.record_usage(
            user_id=user_id,
            conversation_id=conversation_id,
            provider=request.provider.value,
            model=provider.model,
            tokens_used=tokens_used,
        )

        # Send completion event
        yield f"data: {json.dumps({'done': True, 'tokens_used': tokens_used})}\n\n"

    except Exception as e:
        logger.error(f"Streaming error: {str(e)}", exc_info=True)
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@router.get("/conversations")
async def list_conversations(
    user_id: str = Depends(get_current_user_id),
):
    """List user's conversations.

    Args:
        user_id: Current user ID

    Returns:
        List of conversations
    """
    try:
        supabase = get_supabase_client()
        response = (
            supabase.table("conversations")
            .select("*")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .execute()
        )

        return {"conversations": response.data}

    except Exception as e:
        logger.error(f"Failed to list conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations",
        )


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """Get messages for a conversation.

    Args:
        conversation_id: Conversation ID
        user_id: Current user ID

    Returns:
        List of messages

    Raises:
        HTTPException: If conversation not found or unauthorized
    """
    try:
        supabase = get_supabase_client()

        # Verify conversation belongs to user
        conversation = (
            supabase.table("conversations")
            .select("*")
            .eq("id", conversation_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if not conversation.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

        # Get messages
        messages = (
            supabase.table("messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)
            .execute()
        )

        return {"messages": messages.data}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages",
        )
