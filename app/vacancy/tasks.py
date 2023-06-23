from main.celery import app
from vacancy.utils import SkillsCleaner, RequirementsCleaner


@app.task
def full_skills_clean() -> None:
    SkillsCleaner().clean()


@app.task
def full_requirements_clean() -> None:
    RequirementsCleaner().clean()
