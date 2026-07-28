"""Celery configuration and task definitions for CareerOS."""

from celery import Celery
from celery.schedules import crontab
from src.shared.utils.config import get_settings

settings = get_settings()

# Celery Configuration
celery_app = Celery(
    'careeros',
    broker=settings.celery_broker,
    backend=settings.celery_broker,
    include=['src.infrastructure.tasks.tasks']
)

# Celery Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Periodic Tasks Schedule
celery_app.conf.beat_schedule = {
    # Daily job search at 8 AM UTC
    'daily-job-search': {
        'task': 'src.infrastructure.tasks.tasks.run_daily_job_search',
        'schedule': crontab(hour=8, minute=0),
    },
    # Weekly analytics report every Monday at 9 AM UTC
    'weekly-analytics-report': {
        'task': 'src.infrastructure.tasks.tasks.generate_weekly_analytics',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
    # Check follow-ups every 6 hours
    'check-follow-ups': {
        'task': 'src.infrastructure.tasks.tasks.process_follow_up_reminders',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # Resume refresh reminder every Sunday at 10 AM UTC
    'resume-refresh-reminder': {
        'task': 'src.infrastructure.tasks.tasks.send_resume_refresh_reminder',
        'schedule': crontab(hour=10, minute=0, day_of_week=0),
    },
}


if __name__ == '__main__':
    celery_app.start()
