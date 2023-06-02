from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from offer.models.offer import Offer
from profiles.models.startup import Startup


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
