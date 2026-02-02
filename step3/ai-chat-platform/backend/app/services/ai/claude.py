"""Anthropic Claude AI provider implementation."""

import logging
from typing import AsyncGenerator, Dict, List

from anthropic import AsyncAnthropic

from app.models.schemas import ChatMessage
from app.services.ai.base import BaseAIProvider

logger = logging.getLogger(__name__)


class ClaudeProvider(BaseAIProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str, model: str | None = None):
        """Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model: Model name (defaults to claude-3-5-sonnet-20241022)
        """
        super().__init__(api_key, model)
        self.client = AsyncAnthropic(api_key=api_key)

    def get_default_model(self) -> str:
        """Get default Claude model.

        Returns:
            Default model name
        """
        return "claude-sonnet-4-20250514"

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> Dict[str, any]:
        """Generate non-streaming response from Claude.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content, tokens, and finish reason
        """
        try:
            # Convert messages to Claude format
            formatted_messages = self.messages_to_provider_format(messages)

            # Create message
            response = await self.client.messages.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens or 4096,
            )

            return {
                "content": response.content[0].text,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "finish_reason": response.stop_reason,
            }

        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            raise

    async def stream_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from Claude.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks as they arrive
        """
        try:
            # Convert messages to Claude format
            formatted_messages = self.messages_to_provider_format(messages)

            # Stream message
            async with self.client.messages.stream(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens or 4096,
            ) as stream:
                async for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Claude streaming error: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count (rough approximation: 1 token ~= 4 chars)
        """
        # This is a rough approximation
        # For production, use the official tokenizer
        return len(text) // 4
