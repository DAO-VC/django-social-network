from django.db import models
from core.admin import User
from image.models import Image
from profiles.models.other_models import Industries


class Network(models.Model):
    owner = models.OneToOneField(
        User,
        related_name="network_owner",
        on_delete=models.CASCADE,
        verbose_name="Владелец аккаунта",
    )
    logo = models.ForeignKey(
        Image,
        models.SET_NULL,
        verbose_name="Фото профиля",
        null=True,
        blank=True,
        related_name="network_logo",
    )
    interests = models.ManyToManyField(
        Industries,
        verbose_name="Интересы",
        blank=True,
        related_name="scope_of_interest",
    )
    is_active = models.BooleanField(verbose_name="Активен", null=True, blank=True)
    about = models.TextField(verbose_name="О себе")
    connect_network = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Сопряженный Network",
    )

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Networks"

    def __str__(self):
        return f"{self.id} - Network"

    def change_active(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
