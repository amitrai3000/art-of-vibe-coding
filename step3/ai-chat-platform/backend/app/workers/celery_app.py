"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "ai_chat_platform",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.tasks"],
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    "aggregate-usage-hourly": {
        "task": "app.workers.tasks.aggregate_usage",
        "schedule": crontab(minute=0),  # Every hour
    },
    "check-quota-warnings": {
        "task": "app.workers.tasks.check_quota_warnings",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM UTC
    },
    "process-stripe-invoices": {
        "task": "app.workers.tasks.process_stripe_invoices",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),  # 1st of month
    },
}
