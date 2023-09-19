import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
app = Celery("main")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "tags_clean": {
        "task": "articles.tasks.tags_cleaner",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
        # "schedule": crontab(minute="*/1"),
    },
    "images_clean": {
        "task": "articles.tasks.full_image_clean",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    },
    "skills_clean": {
        "task": "vacancy.tasks.full_skills_clean",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    },
    "requirements_clean": {
        "task": "vacancy.tasks.full_requirements_clean",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    },
    # "create_all_networks_connect": {
    #     "task": "network.tasks.connect_network",
    #     # "schedule": crontab(day_of_week='0,2,4,6', ),
    #     "schedule": crontab(minute="*/1"),
    # },
}
