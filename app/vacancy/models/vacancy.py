from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from profiles.models.other_models import Industries


# class Vacancy(models.Model):
#     """Сущность вакансии стартапа"""
#
#     company_id = models.ForeignKey("profiles.Startup", models.CASCADE)
#     position = models.CharField("Позиция", max_length=32)
#     requirements = models.CharField("Требования", max_length=32)
#     is_visible = models.BooleanField(verbose_name="Активен")
#     salary = models.IntegerField(verbose_name="Зарплата")
#     skills = models.ManyToManyField(
#         Industries, verbose_name="Скилы", blank=True, related_name="vacancy_skills"
#     )
#     created_at = CreationDateTimeField(verbose_name="Дата создания")
#     # TODO: обязательные поля


class Vacancy(models.Model):
    """Сущность вакансии стартапа"""

    class SalaryType(models.TextChoices):
        HOURLY = "hourly", "почасовая"
        MONTHLY = "monthly", "ежемесячно"
        ANNUAL = "annual", "ежегодно"
        PER_PROJECT = "perProject", "за проект"

    class WorkSchedude(models.TextChoices):
        FULL_TIME = "fullTime", "полная занятость"
        PART_TIME = "partTime", "частичная занятость"

    class WorkPlace(models.TextChoices):
        OFFICE = "office", "офис"
        REMOTE = "remote", "дистанционная работа"

    company_id = models.ForeignKey("profiles.Startup", models.CASCADE)
    position = models.CharField("Позиция", max_length=32)
    salary = models.IntegerField(verbose_name="Зарплата")
    salary_type = models.CharField(
        "Вид оплаты", choices=SalaryType.choices, max_length=32
    )
    work_schedude = models.CharField(
        "Тип занятости", choices=WorkSchedude.choices, max_length=32
    )
    place = models.CharField(
        "Рабочая локация", choices=WorkPlace.choices, max_length=32
    )
    skills = models.ManyToManyField(
        Industries, verbose_name="Скилы", blank=True, related_name="vacancy_skills"
    )
    # TODO : скилы будут реализованы как тэги
    description = models.TextField("Описание")
    requirements = models.TextField("Требования")
    is_visible = models.BooleanField(verbose_name="Активен")
    created_at = CreationDateTimeField(verbose_name="Дата создания")
    # TODO: обязательные поля
