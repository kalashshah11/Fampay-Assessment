import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import register_events

from app.youtube_ingest import youtube_search

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    settings.SCHEDULER_AUTOSTART = 0
    scheduler.remove_all_jobs()
    scheduler.add_job(youtube_search, 'interval', seconds=int(os.getenv("INTERVAL")), replace_existing=True,
                      id="youtube_search")
    register_events(scheduler)
    scheduler.start()
