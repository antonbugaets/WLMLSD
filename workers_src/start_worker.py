from celery import Celery
import os

celery_app = Celery(
    "TextMorph",
    broker=os.getenv("BROKER_URL"),
    backend=os.getenv("BACKEND_URL"),
    include="TBD",
)

celery_app.conf.task_track_started = True
