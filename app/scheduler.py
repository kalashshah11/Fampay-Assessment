import logging
import os

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from pymongo import MongoClient
from pytz import utc

from app.youtube_ingest import youtube_search

client = MongoClient(host="mongodb://127.0.0.1", port=27017)
jobstores = {
    'default': MongoDBJobStore(client=client, database="fampay"),
}
executors = {
    'default': ThreadPoolExecutor(1),
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=utc)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    if os.getenv("SCHEDULER_START") == "1":
        scheduler.remove_all_jobs()
        scheduler.add_job(youtube_search, 'interval', seconds=int(os.getenv("INTERVAL")), replace_existing=True,
                          id="youtube_search")
    scheduler.start()
