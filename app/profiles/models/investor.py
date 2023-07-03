from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import User
from image.models import Image, File
from profiles.models.other_models import Industries


class Investor(models.Model):
    """Модель сущности инвестор"""

    owner = models.ForeignKey(User, models.CASCADE, verbose_name="Владелец")
    name = models.CharField("Имя", max_length=32)
    lastName = models.CharField("Фамилия", max_length=32)
    email = models.EmailField("Email адрес")
    phone = PhoneNumberField(
        max_length=128, verbose_name="Номер телефона", null=True, blank=True
    )
    about = models.TextField(verbose_name="Обо мне", null=True, blank=True)
    photo = models.ForeignKey(
        Image, models.SET_NULL, verbose_name="Фото", null=True, blank=True
    )
    interest = models.ManyToManyField(
        Industries,
        verbose_name="Интересы",
        blank=True,
        related_name="invest_interest",
    )
    cv = models.ForeignKey(
        File, models.SET_NULL, verbose_name="Файл презентации", null=True, blank=True
    )
    social_links = models.ForeignKey(
        "Links", models.SET_NULL, verbose_name="Социальные сети", null=True, blank=True
    )

    class Meta:
        verbose_name = "Инвестор"
        verbose_name_plural = "Инвесторы"

    def __str__(self):
        return f"{self.id} - {self.name}"
