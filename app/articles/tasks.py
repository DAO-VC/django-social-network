from articles.utils import TagsCleaner
from main.celery import app


@app.task
def tags_cleaner() -> None:
    TagsCleaner().clean()
