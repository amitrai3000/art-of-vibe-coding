"""AI provider factory."""

from app.config import get_settings
from app.models.schemas import AIProvider
from app.services.ai.base import BaseAIProvider
from app.services.ai.claude import ClaudeProvider
from app.services.ai.gemini import GeminiProvider
from app.services.ai.openai import OpenAIProvider


class AIProviderFactory:
    """Factory for creating AI provider instances."""

    @staticmethod
    def create_provider(
        provider: AIProvider,
        model: str | None = None,
    ) -> BaseAIProvider:
        """Create an AI provider instance.

        Args:
            provider: AI provider type
            model: Optional model name to override default

        Returns:
            Configured AI provider instance

        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        settings = get_settings()

        if provider == AIProvider.CLAUDE:
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return ClaudeProvider(
                api_key=settings.anthropic_api_key,
                model=model,
            )

        elif provider == AIProvider.OPENAI:
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider(
                api_key=settings.openai_api_key,
                model=model,
            )

        elif provider == AIProvider.GEMINI:
            if not settings.google_api_key:
                raise ValueError("Google API key not configured")
            return GeminiProvider(
                api_key=settings.google_api_key,
                model=model,
            )

        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
