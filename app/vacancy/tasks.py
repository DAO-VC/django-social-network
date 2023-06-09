from main.celery import app
from vacancy.utils import SkillsCleaner


@app.task
def full_skills_clean() -> None:
    SkillsCleaner().clean()
