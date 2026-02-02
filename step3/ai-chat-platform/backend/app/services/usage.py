"""Usage tracking service."""

import logging
from datetime import datetime
from typing import Dict

from app.db.supabase import get_supabase_client

logger = logging.getLogger(__name__)


class UsageService:
    """Service for tracking AI usage."""

    def __init__(self):
        """Initialize usage service."""
        self.supabase = get_supabase_client()

    async def record_usage(
        self,
        user_id: str,
        conversation_id: str,
        provider: str,
        model: str,
        tokens_used: int,
        cost_usd: float = 0.0,
    ) -> None:
        """Record AI usage for a user.

        Args:
            user_id: User ID
            conversation_id: Conversation ID
            provider: AI provider name
            model: Model name
            tokens_used: Number of tokens used
            cost_usd: Estimated cost in USD
        """
        try:
            self.supabase.table("usage_records").insert(
                {
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "provider": provider,
                    "model": model,
                    "tokens_used": tokens_used,
                    "cost_usd": cost_usd,
                    "created_at": datetime.utcnow().isoformat(),
                }
            ).execute()

            logger.info(
                f"Recorded usage for user {user_id}: {tokens_used} tokens "
                f"({provider}/{model})"
            )

        except Exception as e:
            logger.error(f"Failed to record usage: {str(e)}")
            # Don't raise - usage tracking shouldn't break the main flow

    async def get_user_usage(self, user_id: str, period_days: int = 30) -> Dict:
        """Get usage statistics for a user.

        Args:
            user_id: User ID
            period_days: Number of days to look back

        Returns:
            Dictionary with usage statistics
        """
        try:
            # Get usage records
            response = (
                self.supabase.table("usage_records")
                .select("*")
                .eq("user_id", user_id)
                .gte(
                    "created_at",
                    datetime.utcnow().replace(day=1).isoformat(),
                )
                .execute()
            )

            records = response.data

            # Calculate statistics
            total_tokens = sum(r["tokens_used"] for r in records)
            total_cost = sum(r["cost_usd"] for r in records)

            # Group by provider
            by_provider = {}
            for record in records:
                provider = record["provider"]
                if provider not in by_provider:
                    by_provider[provider] = {
                        "tokens": 0,
                        "cost": 0.0,
                        "requests": 0,
                    }
                by_provider[provider]["tokens"] += record["tokens_used"]
                by_provider[provider]["cost"] += record["cost_usd"]
                by_provider[provider]["requests"] += 1

            return {
                "total_messages": len(records),
                "total_tokens": total_tokens,
                "total_cost_usd": total_cost,
                "by_provider": by_provider,
            }

        except Exception as e:
            logger.error(f"Failed to get user usage: {str(e)}")
            return {
                "total_messages": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "by_provider": {},
            }
