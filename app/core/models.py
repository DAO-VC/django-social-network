from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.managers import UserManager


class User(AbstractUser):
    """Базовая модель пользователя"""

    class UserProfile(models.TextChoices):
        STARTUP = "startup", "Стартап"
        INVESTOR = "investor", "Инвестор"
        PROFESSIONAL = "professional", "Профессионал"

    email = models.EmailField(_("email address"), blank=True, unique=True)
    phone = PhoneNumberField(
        max_length=128, verbose_name="Номер телефона", blank=True, null=True
    )
    code = models.CharField(max_length=7, null=True, blank=True)
    # Get rid of all references to the username field
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
    )
    is_onboarding = models.BooleanField(
        verbose_name="Онбоардинг", null=True, blank=True
    )
    objects = UserManager()
    profile = models.CharField("Профиль", choices=UserProfile.choices, max_length=12)
    permissions = models.ForeignKey(
        "vacancy.WorkTeam", models.SET_NULL, null=True, blank=True
    )
    online = models.BooleanField(default=False, verbose_name="Онлайн статус")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.id} - {self.email}"
