from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_puzzle.settings')

app = Celery('daily_puzzle')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Schedule
app.conf.beat_schedule = {
    'generate-daily-puzzle': {
        'task': 'puzzles.tasks.generate_daily_puzzle',
        'schedule': crontab(hour=0, minute=0),  # Every day at 00:00 UTC
    },
    'evaluate-daily-results': {
        'task': 'puzzles.tasks.evaluate_daily_results',
        'schedule': crontab(hour=23, minute=59),  # Every day at 23:59 UTC
    },
    'cleanup-old-puzzles': {
        'task': 'puzzles.tasks.cleanup_old_puzzles',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Weekly on Sunday at 02:00
    },
    'test-ai-models': {
        'task': 'puzzles.tasks.test_ai_models',
        'schedule': crontab(hour=12, minute=0),  # Daily at noon for monitoring
    },
}

app.conf.timezone = 'UTC'
app.autodiscover_tasks()