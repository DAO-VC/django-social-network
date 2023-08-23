from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from offer.models.offer import Offer
from profiles.models.startup import Startup


class CandidateStartup(models.Model):
    class AcceptStatus(models.TextChoices):
        DECLINE = "decline", "Отклонен"
        CONCLUDED = "concluded", "Исключен"
        PENDING_FOR_APPROVAL = "pendingforapproval", "Подал заявку"
        ACCEPT = "accept", "Подтвержден"

    startup_id = models.ForeignKey(
        Startup, models.CASCADE, related_name="startup_to_offer"
    )
    offer_id = models.ForeignKey(
        Offer, models.SET_NULL, related_name="offer_to_candidate", null=True
    )

    accept_status = models.CharField(
        "Статус", choices=AcceptStatus.choices, max_length=50, null=True, blank=True
    )
    about = models.TextField("Обо мне")
    is_favorite = models.BooleanField(verbose_name="В избранных")
    created_at = CreationDateTimeField(verbose_name="Дата создания")

    class Meta:
        unique_together = (
            "startup_id",
            "offer_id",
        )

    def __str__(self):
        return f"{self.id} - Кандидат"

    def change_favorite(self):
        if self.is_favorite:
            self.is_favorite = False
        else:
            self.is_favorite = True
