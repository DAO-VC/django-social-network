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
        PERCENT = "percent", "процент"

    class WorkSchedude(models.TextChoices):
        FULL_TIME = "fullTime", "полная занятость"
        PART_TIME = "partTime", "частичная занятость"
        PROJECT = "project", "проектная занятость"

    class WorkPlace(models.TextChoices):
        OFFICE = "office", "офис"
        REMOTE = "remote", "дистанционная работа"
        MIXED = "mixed", "смешанный тип работы"

    company_id = models.ForeignKey("profiles.Startup", models.CASCADE)
    position = models.CharField("Позиция", max_length=32)
    salary = models.IntegerField(verbose_name="Зарплата", null=True, blank=True)
    salary_type = models.CharField(
        "Вид оплаты", choices=SalaryType.choices, max_length=32
    )
    work_schedude = models.CharField(
        "Тип занятости", choices=WorkSchedude.choices, max_length=32
    )
    place = models.CharField(
        "Рабочая локация", choices=WorkPlace.choices, max_length=32
    )
    skills = models.ManyToManyField("Skill", related_name="vacancy_skills", blank=True)

    description = models.TextField("Описание")
    requirements = models.ManyToManyField(
        "Requirement", related_name="vacancy_requirements", blank=True
    )
    is_visible = models.BooleanField(verbose_name="Активен")
    created_at = CreationDateTimeField(verbose_name="Дата создания")

    # TODO: обязательные поля
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]


class Skill(models.Model):
    title = models.CharField("Заголовок", max_length=32)

    def __str__(self):
        return self.title


class Requirement(models.Model):
    title = models.CharField("Заголовок", max_length=32)

    def __str__(self):
        return self.title
