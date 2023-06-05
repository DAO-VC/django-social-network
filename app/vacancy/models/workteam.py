from django.db import models
from vacancy.models.candidate import Candidate


class WorkTeam(models.Model):
    """Сущность - участник команды стартапа"""

    candidate_id = models.ForeignKey(Candidate, models.CASCADE)
    startup_id = models.ForeignKey("profiles.Startup", models.CASCADE)
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

    class Meta:
        unique_together = (
            "startup_id",
            "candidate_id",
        )
