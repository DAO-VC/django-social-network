from django.db import models

from profiles.models import Startup, Industries, Investor


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
