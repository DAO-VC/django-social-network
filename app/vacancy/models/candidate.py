from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from profiles.models.professional import Professional
from vacancy.models.vacancy import Vacancy


class Candidate(models.Model):
    """Сущность кандидата на вакансию стартапа"""

    class BaseStatus(models.TextChoices):
        NEW = "new", "Новый"
        VIEWED = "viewed", "Просмотрен"

    class AcceptStatus(models.TextChoices):
        DECLINE = "decline", "Отклонен"
        PENDING_FOR_APPROVAL = "pendingforapproval", "Подал заявку"
        IN_THE_TEAM = "intheteam", "В команде"

    professional_id = models.ForeignKey(Professional, models.CASCADE)
    vacancy_id = models.ForeignKey(Vacancy, models.CASCADE)
    about = models.TextField("Обо мне")
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
    is_favorite = models.BooleanField(verbose_name="В избранных")
    created_at = CreationDateTimeField(verbose_name="Дата создания")

    class Meta:
        unique_together = (
            "professional_id",
            "vacancy_id",
        )

    def change_favorite(self):
        if self.is_favorite:
            self.is_favorite = False
        else:
            self.is_favorite = True
