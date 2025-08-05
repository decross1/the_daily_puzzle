"""
Celery configuration for daily_puzzle project.
"""
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_puzzle.settings')

app = Celery('daily_puzzle')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Beat schedule for daily puzzle generation
app.conf.beat_schedule = {
    'generate-daily-puzzle': {
        'task': 'puzzles.tasks.generate_daily_puzzle',
        'schedule': 60.0,  # Every minute for testing, should be daily
        'options': {'timezone': 'UTC'}
    },
    'evaluate-daily-results': {
        'task': 'puzzles.tasks.evaluate_daily_results',
        'schedule': 3540.0,  # 59 minutes for testing, should be 23:59 UTC
        'options': {'timezone': 'UTC'}
    },
}