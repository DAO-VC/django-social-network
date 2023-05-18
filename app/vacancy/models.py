from django.db import models

from profiles.models import Startup, Industries, Investor, Professional


class Vacancy(models.Model):
    company_id = models.ForeignKey(Startup, models.CASCADE)
    position = models.CharField("Позиция", max_length=32)
    requirements = models.CharField("Требования", max_length=32)
    is_active = models.BooleanField(verbose_name="Активен")
    salary = models.IntegerField(verbose_name="Зарплата")
    skills = models.ManyToManyField(
        Industries, verbose_name="Скилы", blank=True, related_name="vacancy_skills"
    )
    # TODO: обязательные поля


class Offer(models.Model):
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


class Candidate(models.Model):
    class BaseStatus(models.TextChoices):
        NEW = "new", "Новый"
        VIEWED = "viewed", "Просмотрен"

    class AcceptStatus(models.TextChoices):
        PENDING_FOR_APPROVAL = "pendingforapproval", "Подал заявку"
        APPROVE = "approve", "Подтвержден"
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

    class Meta:
        unique_together = (
            "professional_id",
            "vacancy_id",
        )
