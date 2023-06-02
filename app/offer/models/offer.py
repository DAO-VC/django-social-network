from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from profiles.models.investor import Investor
from profiles.models.other_models import Industries
from profiles.models.startup import Startup


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


class ConfirmedOffer(models.Model):
    startup_id = models.ForeignKey(Startup, models.CASCADE)
    investor_id = models.ForeignKey(Investor, models.CASCADE)

    class Meta:
        unique_together = (
            "startup_id",
            "investor_id",
        )
