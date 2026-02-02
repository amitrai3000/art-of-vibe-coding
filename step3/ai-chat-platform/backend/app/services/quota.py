"""Quota enforcement service."""

import logging
from typing import Dict

from app.db.supabase import get_supabase_client

logger = logging.getLogger(__name__)


# Quota limits by tier (tokens per month)
TIER_LIMITS = {
    "free": 100_000,
    "pro": 1_000_000,
    "enterprise": 10_000_000,
}


class QuotaService:
    """Service for enforcing usage quotas."""

    def __init__(self):
        """Initialize quota service."""
        self.supabase = get_supabase_client()

    async def check_quota(self, user_id: str) -> Dict[str, any]:
        """Check if user has quota available.

        Args:
            user_id: User ID

        Returns:
            Dictionary with quota information and availability
        """
        try:
            # Get user profile with subscription tier
            profile_response = (
                self.supabase.table("user_profiles")
                .select("subscription_tier")
                .eq("user_id", user_id)
                .single()
                .execute()
            )

            tier = profile_response.data.get("subscription_tier", "free")
            limit = TIER_LIMITS.get(tier, TIER_LIMITS["free"])

            # Get current month usage
            usage_response = (
                self.supabase.rpc("get_monthly_usage", {"p_user_id": user_id})
                .execute()
            )

            tokens_used = usage_response.data or 0
            tokens_remaining = max(0, limit - tokens_used)

            return {
                "tier": tier,
                "tokens_limit": limit,
                "tokens_used": tokens_used,
                "tokens_remaining": tokens_remaining,
                "has_quota": tokens_remaining > 0,
            }

        except Exception as e:
            logger.error(f"Failed to check quota: {str(e)}")
            # On error, allow request but log
            return {
                "tier": "unknown",
                "tokens_limit": 0,
                "tokens_used": 0,
                "tokens_remaining": 0,
                "has_quota": True,  # Fail open
            }

    async def enforce_quota(self, user_id: str, estimated_tokens: int = 1000) -> None:
        """Enforce quota before making AI request.

        Args:
            user_id: User ID
            estimated_tokens: Estimated tokens for the request

        Raises:
            ValueError: If user has exceeded quota
        """
        quota_info = await self.check_quota(user_id)

        if not quota_info["has_quota"]:
            raise ValueError(
                f"Quota exceeded. You have used {quota_info['tokens_used']} "
                f"of your {quota_info['tokens_limit']} token limit for the "
                f"{quota_info['tier']} tier this month."
            )

        if quota_info["tokens_remaining"] < estimated_tokens:
            logger.warning(
                f"User {user_id} is close to quota limit: "
                f"{quota_info['tokens_remaining']} tokens remaining"
            )
