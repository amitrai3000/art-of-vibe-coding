"""OpenAI AI provider implementation."""

import logging
from typing import AsyncGenerator, Dict, List

from openai import AsyncOpenAI

from app.models.schemas import ChatMessage
from app.services.ai.base import BaseAIProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider."""

    def __init__(self, api_key: str, model: str | None = None):
        """Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name (defaults to gpt-4-turbo-preview)
        """
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key)

    def get_default_model(self) -> str:
        """Get default OpenAI model.

        Returns:
            Default model name
        """
        return "gpt-4-turbo-preview"

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> Dict[str, any]:
        """Generate non-streaming response from OpenAI.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content, tokens, and finish reason
        """
        try:
            # Convert messages to OpenAI format
            formatted_messages = self.messages_to_provider_format(messages)

            # Create chat completion
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            choice = response.choices[0]
            return {
                "content": choice.message.content,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": choice.finish_reason,
            }

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

    async def stream_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from OpenAI.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks as they arrive
        """
        try:
            # Convert messages to OpenAI format
            formatted_messages = self.messages_to_provider_format(messages)

            # Stream chat completion
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"OpenAI streaming error: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count (rough approximation: 1 token ~= 4 chars)
        """
        # This is a rough approximation
        # For production, use tiktoken library
        return len(text) // 4
