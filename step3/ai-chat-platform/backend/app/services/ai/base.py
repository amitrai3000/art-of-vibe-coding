"""Base AI provider interface."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List

from app.models.schemas import ChatMessage


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: str, model: str | None = None):
        """Initialize AI provider.

        Args:
            api_key: API key for the provider
            model: Default model name to use
        """
        self.api_key = api_key
        self.model = model or self.get_default_model()

    @abstractmethod
    def get_default_model(self) -> str:
        """Get default model name for this provider.

        Returns:
            Default model name
        """
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> Dict[str, any]:
        """Generate a non-streaming response.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary with 'content', 'tokens_used', 'finish_reason'
        """
        pass

    @abstractmethod
    async def stream_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 1.0,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response.

        Args:
            messages: List of chat messages
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate

        Yields:
            Content chunks as they are generated
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        pass

    def messages_to_provider_format(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert messages to provider-specific format.

        Args:
            messages: List of ChatMessage objects

        Returns:
            List of message dictionaries
        """
        return [{"role": msg.role.value, "content": msg.content} for msg in messages]
