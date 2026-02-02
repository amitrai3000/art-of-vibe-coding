"""Google Gemini AI provider implementation."""

import logging
from typing import AsyncGenerator, Dict, List

import google.generativeai as genai

from app.models.schemas import ChatMessage
from app.services.ai.base import BaseAIProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):
    """Google Gemini provider."""

    def __init__(self, api_key: str, model: str | None = None):
        """Initialize Gemini provider.

        Args:
            api_key: Google API key
            model: Model name (defaults to gemini-pro)
        """
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(self.model)

    def get_default_model(self) -> str:
        """Get default Gemini model.

        Returns:
            Default model name
        """
        return "gemini-2.0-flash"

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> Dict[str, any]:
        """Generate non-streaming response from Gemini.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Response dictionary with content, tokens, and finish reason
        """
        try:
            # Convert messages to Gemini format (concatenate for now)
            # Gemini has different message handling, this is simplified
            prompt = "\n\n".join(
                [f"{msg.role.value}: {msg.content}" for msg in messages]
            )

            # Generate content
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )

            # Extract token counts if available
            tokens_used = 0
            if hasattr(response, "usage_metadata"):
                tokens_used = (
                    response.usage_metadata.prompt_token_count
                    + response.usage_metadata.candidates_token_count
                )

            return {
                "content": response.text,
                "tokens_used": tokens_used,
                "finish_reason": "stop",
            }

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    async def stream_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Stream response from Gemini.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks as they arrive
        """
        try:
            # Convert messages to Gemini format
            prompt = "\n\n".join(
                [f"{msg.role.value}: {msg.content}" for msg in messages]
            )

            # Stream content
            response = await self.client.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
                stream=True,
            )

            async for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Gemini streaming error: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to estimate tokens for

        Returns:
            Estimated token count (rough approximation: 1 token ~= 4 chars)
        """
        # This is a rough approximation
        return len(text) // 4
