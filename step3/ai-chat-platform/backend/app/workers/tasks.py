"""Celery background tasks."""

import logging
from datetime import datetime, timedelta

import stripe
from resend import Resend

from app.config import get_settings
from app.db.supabase import get_supabase_client
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize services
if settings.stripe_secret_key:
    stripe.api_key = settings.stripe_secret_key

if settings.resend_api_key:
    resend_client = Resend(api_key=settings.resend_api_key)


@celery_app.task(name="app.workers.tasks.aggregate_usage")
def aggregate_usage() -> dict:
    """Aggregate usage statistics for all users.

    This task runs hourly to update usage summaries.

    Returns:
        Dictionary with aggregation results
    """
    try:
        logger.info("Starting usage aggregation...")
        supabase = get_supabase_client()

        # Get current hour's usage
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)

        response = (
            supabase.table("usage_records")
            .select("user_id, tokens_used, cost_usd")
            .gte("created_at", one_hour_ago.isoformat())
            .execute()
        )

        records = response.data
        logger.info(f"Aggregating {len(records)} usage records")

        # Group by user and update aggregates
        # This is simplified - in production, use a dedicated aggregates table
        user_totals = {}
        for record in records:
            user_id = record["user_id"]
            if user_id not in user_totals:
                user_totals[user_id] = {"tokens": 0, "cost": 0.0}
            user_totals[user_id]["tokens"] += record["tokens_used"]
            user_totals[user_id]["cost"] += record["cost_usd"]

        logger.info(f"Aggregated usage for {len(user_totals)} users")

        return {
            "status": "success",
            "records_processed": len(records),
            "users_updated": len(user_totals),
        }

    except Exception as e:
        logger.error(f"Usage aggregation failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}


@celery_app.task(name="app.workers.tasks.check_quota_warnings")
def check_quota_warnings() -> dict:
    """Check for users approaching quota limits and send warnings.

    Returns:
        Dictionary with task results
    """
    try:
        logger.info("Checking quota warnings...")
        supabase = get_supabase_client()

        # Get users at 80% or 90% of quota
        # This is simplified - implement proper quota checking
        response = supabase.rpc("get_users_near_quota").execute()

        users_to_notify = response.data or []
        emails_sent = 0

        for user in users_to_notify:
            try:
                # Send warning email
                if settings.resend_api_key:
                    resend_client.emails.send(
                        {
                            "from": settings.resend_from_email,
                            "to": user["email"],
                            "subject": "AI Chat Platform - Quota Warning",
                            "html": f"""
                            <h2>Usage Alert</h2>
                            <p>You have used {user['usage_percent']}% of your monthly quota.</p>
                            <p>Current usage: {user['tokens_used']:,} tokens</p>
                            <p>Monthly limit: {user['tokens_limit']:,} tokens</p>
                            <p>Consider upgrading your plan to continue using the service.</p>
                            """,
                        }
                    )
                    emails_sent += 1

            except Exception as e:
                logger.error(f"Failed to send email to {user['email']}: {str(e)}")

        logger.info(f"Sent {emails_sent} quota warning emails")

        return {
            "status": "success",
            "users_checked": len(users_to_notify),
            "emails_sent": emails_sent,
        }

    except Exception as e:
        logger.error(f"Quota warning check failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}


@celery_app.task(name="app.workers.tasks.process_stripe_invoices")
def process_stripe_invoices() -> dict:
    """Process Stripe invoices for usage-based billing.

    This runs on the 1st of each month.

    Returns:
        Dictionary with processing results
    """
    try:
        logger.info("Processing Stripe invoices...")
        supabase = get_supabase_client()

        if not settings.stripe_secret_key:
            logger.warning("Stripe not configured, skipping invoice processing")
            return {"status": "skipped", "reason": "stripe_not_configured"}

        # Get all paid users with usage in the previous month
        last_month = datetime.utcnow().replace(day=1) - timedelta(days=1)

        response = (
            supabase.rpc(
                "get_monthly_usage_by_user",
                {"p_month": last_month.strftime("%Y-%m")},
            )
            .execute()
        )

        users_usage = response.data or []
        invoices_created = 0

        for user_usage in users_usage:
            try:
                # Create Stripe usage record
                if user_usage.get("stripe_customer_id") and user_usage.get("cost_usd", 0) > 0:
                    stripe.InvoiceItem.create(
                        customer=user_usage["stripe_customer_id"],
                        amount=int(user_usage["cost_usd"] * 100),  # Convert to cents
                        currency="usd",
                        description=f"AI Chat Platform - {last_month.strftime('%B %Y')}",
                    )
                    invoices_created += 1

            except Exception as e:
                logger.error(
                    f"Failed to create invoice for user {user_usage['user_id']}: {str(e)}"
                )

        logger.info(f"Created {invoices_created} Stripe invoices")

        return {
            "status": "success",
            "users_processed": len(users_usage),
            "invoices_created": invoices_created,
        }

    except Exception as e:
        logger.error(f"Stripe invoice processing failed: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}


@celery_app.task(name="app.workers.tasks.send_usage_report")
def send_usage_report(user_id: str, email: str) -> dict:
    """Send usage report email to a user.

    Args:
        user_id: User ID
        email: User email address

    Returns:
        Task result dictionary
    """
    try:
        logger.info(f"Sending usage report to {email}")
        supabase = get_supabase_client()

        # Get user's usage stats
        response = supabase.rpc("get_monthly_usage", {"p_user_id": user_id}).execute()

        usage = response.data or {}

        # Send email
        if settings.resend_api_key:
            resend_client.emails.send(
                {
                    "from": settings.resend_from_email,
                    "to": email,
                    "subject": "Your AI Chat Platform Usage Report",
                    "html": f"""
                    <h2>Monthly Usage Report</h2>
                    <p>Total tokens used: {usage.get('total_tokens', 0):,}</p>
                    <p>Total messages: {usage.get('total_messages', 0):,}</p>
                    <p>Total cost: ${usage.get('total_cost_usd', 0):.2f}</p>
                    """,
                }
            )

        return {"status": "success", "email": email}

    except Exception as e:
        logger.error(f"Failed to send usage report: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}
