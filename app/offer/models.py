from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from profiles.models import Investor, Industries


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
    # TODO: article?
    created_at = CreationDateTimeField(verbose_name="Дата создания")
