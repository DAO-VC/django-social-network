from django.db import models
from django_extensions.db.fields import CreationDateTimeField


class Vacancy(models.Model):
    """Сущность вакансии стартапа"""

    class ActiveStatus(models.TextChoices):
        ACTIVE = "active", "активна"
        ARCHIVE = "archive", "в архиве"

    class SalaryType(models.TextChoices):
        HOURLY = "hourly", "почасовая"
        MONTHLY = "monthly", "ежемесячно"
        ANNUAL = "annual", "ежегодно"
        PER_PROJECT = "perProject", "за проект"
        PERCENT = "percent", "процент"

    class WorkSchedule(models.TextChoices):
        FULL_TIME = "fullTime", "полная занятость"
        PART_TIME = "partTime", "частичная занятость"
        PROJECT = "project", "проектная занятость"

    class WorkPlace(models.TextChoices):
        OFFICE = "office", "офис"
        REMOTE = "remote", "дистанционная работа"
        MIXED = "mixed", "смешанный тип работы"

    company_id = models.ForeignKey(
        "profiles.Startup", models.CASCADE, verbose_name="Владелец"
    )
    position = models.CharField("Позиция", max_length=32)
    salary = models.IntegerField(verbose_name="Зарплата", null=True, blank=True)
    salary_type = models.CharField(
        "Вид оплаты", choices=SalaryType.choices, max_length=32
    )
    work_schedule = models.CharField(
        "Тип занятости", choices=WorkSchedule.choices, max_length=32
    )
    place = models.CharField(
        "Рабочая локация", choices=WorkPlace.choices, max_length=32
    )
    skills = models.ManyToManyField(
        "Skill", related_name="vacancy_skills", blank=True, verbose_name="Навыки"
    )

    description = models.TextField("Описание")
    requirements = models.ManyToManyField(
        "Requirement",
        related_name="vacancy_requirements",
        blank=True,
        verbose_name="Требования",
    )
    is_visible = models.BooleanField(verbose_name="Активна")
    created_at = CreationDateTimeField(verbose_name="Дата создания")
    active_status = models.CharField(
        "Активный статус", choices=ActiveStatus.choices, max_length=32
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return f"{self.id} - Вакансия"


class Skill(models.Model):
    """Модель умения"""

    title = models.CharField("Заголовок", max_length=54)

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        verbose_name = "Умение"
        verbose_name_plural = "Умения"


class Requirement(models.Model):
    """Модель требования"""

    title = models.TextField(
        "Заголовок",
    )

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        verbose_name = "Требование"
        verbose_name_plural = "Требования"
