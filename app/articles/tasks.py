from articles.utils import TagsCleaner, ImagesCleaner
from main.celery import app


@app.task
def tags_cleaner() -> None:
    TagsCleaner().clean()


@app.task
def full_image_clean() -> None:
    ImagesCleaner().clean()
