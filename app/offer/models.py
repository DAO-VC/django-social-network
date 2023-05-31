from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from profiles.models import Investor, Industries, Startup


class Offer(models.Model):
    """Сущность оффера инвестора"""

    investor_id = models.ForeignKey(Investor, models.CASCADE)
    amount = models.IntegerField(verbose_name="Кол-во инвестиций")
    industries = models.ManyToManyField(
        Industries,
        verbose_name="Индустрии",
        blank=True,
        related_name="offer_industries",
    )
    details = models.TextField("Детали")
    is_visible = models.BooleanField(verbose_name="Активен")
    # TODO: article?
    created_at = CreationDateTimeField(verbose_name="Дата создания")


class CandidateStartup(models.Model):
    class AcceptStatus(models.TextChoices):
        PENDING_FOR_APPROVAL = "pendingforapproval", "Подал заявку"
        ACCEPT = "accept", "Подтвержден"

    startup_id = models.ForeignKey(Startup, models.CASCADE)
    offer_id = models.ForeignKey(Offer, models.CASCADE)

    accept_status = models.CharField(
        "Статус", choices=AcceptStatus.choices, max_length=50, null=True, blank=True
    )
    created_at = CreationDateTimeField(verbose_name="Дата создания")

    class Meta:
        unique_together = (
            "startup_id",
            "offer_id",
        )
