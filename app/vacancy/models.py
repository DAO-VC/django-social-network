from django.db import models
from django.utils import timezone
from profiles.models import Startup, Industries, Investor, Professional


class Vacancy(models.Model):
    """Сущность вакансии стартапа"""

    company_id = models.ForeignKey(Startup, models.CASCADE)
    position = models.CharField("Позиция", max_length=32)
    requirements = models.CharField("Требования", max_length=32)
    is_visible = models.BooleanField(verbose_name="Активен")
    salary = models.IntegerField(verbose_name="Зарплата")
    skills = models.ManyToManyField(
        Industries, verbose_name="Скилы", blank=True, related_name="vacancy_skills"
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    # TODO: обязательные поля


class Offer(models.Model):
    """Сущность офера инвестора"""

    investor_id = models.ForeignKey(Investor, models.CASCADE)
    amount = models.IntegerField(verbose_name="Кол-во инвестиций")
    industries = models.ManyToManyField(
        Industries,
        verbose_name="Индустрии",
        blank=True,
        related_name="offer_industries",
    )
    details = models.TextField("Детали")
    # TODO: article?
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )


class Candidate(models.Model):
    """Сущность кандидата на вакансию стартапа"""

    class BaseStatus(models.TextChoices):
        NEW = "new", "Новый"
        VIEWED = "viewed", "Просмотрен"

    class AcceptStatus(models.TextChoices):
        PENDING_FOR_APPROVAL = "pendingforapproval", "Подал заявку"
        ACCEPT = "accept", "Подтвержден"
        IN_THE_TEAM = "intheteam", "В команде"

    professional_id = models.ForeignKey(Professional, models.CASCADE)
    vacancy_id = models.ForeignKey(Vacancy, models.CASCADE)
    base_status = models.CharField(
        "Статус просмотра",
        choices=BaseStatus.choices,
        max_length=20,
        null=True,
        blank=True,
    )
    accept_status = models.CharField(
        "Статус", choices=AcceptStatus.choices, max_length=50, null=True, blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )

    class Meta:
        unique_together = (
            "professional_id",
            "vacancy_id",
        )


class WorkTeam(models.Model):
    """Сущность - участник команды стартапа"""

    candidate_id = models.ForeignKey(Candidate, models.CASCADE)
    articles_and_news_management = models.BooleanField(
        verbose_name="Изменение статей и новостей", default=False
    )
    performers_management = models.BooleanField(
        verbose_name="Возможность выдавать права", default=False
    )
    company_management = models.BooleanField(
        verbose_name="Изменение компании", default=False
    )
    vacancy_management = models.BooleanField(
        verbose_name="Изменение статей", default=False
    )
    position = models.CharField("Позиция", max_length=32, blank=True, null=True)


# test
