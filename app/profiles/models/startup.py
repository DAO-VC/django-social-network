from django.db import models

from core.models import User
from image.models import Image, File
from profiles.models.other_models import (
    Industries,
    SaleRegions,
    BusinessType,
    Purpose,
    Achievements,
    Links,
)
from vacancy.models.workteam import WorkTeam


class Startup(models.Model):
    """Модель сущности Стартап"""

    class StageChoices(models.TextChoices):
        SEED = "seed", "Основание"
        PRIVATE = "private", "Приват"
        STRATEGIC = "strategic", "Стратеджик"
        PUBLIC = "public", "Паблик"
        SECONDARY_FUNDRAISING = "secondaryFundraising", "Вторичное финансирование"
        NO_FUNDRAISING_REQUIRED = "noFundraisingRequired", "Финансирование не требуется"

    class BusinessTypes(models.TextChoices):
        B2B = "b2b", "Business to Business"
        B2C = "b2c", "Business to consumer"
        B2G = "b2g", "Business to Government"
        C2B = "c2b", "Consumer to business"
        C2C = "c2c", "Consumer to consumer"
        C2G = "c2g", "Consumer to Government"
        SAAS = "saas", "Software on Demand"

    class CurrentStage(models.TextChoices):
        PROJECT_START = "projectStart", "Старт проекта"
        WORKING_ON_THE_PRODUCT = "workingOnTheProject", "Работа над продуктом"
        ENTERING_THE_MARKET = "enteringTheMarket", "Выход на рынок"
        GROWTH_AND_SCALING = "growthAndScaling", "Рост и масштабирование"

    owner = models.ForeignKey(User, models.CASCADE, verbose_name="Владелец")
    name = models.CharField("Название", max_length=32)
    url = models.TextField("Урл", null=True, blank=True)
    foundation_year = models.IntegerField(
        null=True, blank=True, verbose_name="Год основания"
    )
    short_description = models.TextField(verbose_name="Описание", null=True, blank=True)
    logo = models.ForeignKey(
        Image,
        models.SET_NULL,
        verbose_name="Логотип",
        null=True,
        blank=True,
        related_name="startup_logo",
    )
    background = models.ForeignKey(
        Image,
        models.SET_NULL,
        verbose_name="Бэкграунд",
        null=True,
        blank=True,
        related_name="startup_background",
    )
    industries = models.ManyToManyField(
        Industries, verbose_name="Индустрии", blank=True, related_name="industries"
    )
    is_registered = models.BooleanField(verbose_name="Уже зарегистрирована")

    registration_country = models.ForeignKey(
        SaleRegions,
        models.SET_NULL,
        verbose_name="Страна регистрации",
        null=True,
        blank=True,
        related_name="core_region",
    )
    headquartered = models.CharField(
        "Штаб-квартира", max_length=32, null=True, blank=True
    )
    regions = models.ManyToManyField(
        SaleRegions,
        verbose_name="Регионы продажи",
        blank=True,
        related_name="sale_regions",
    )
    stage = models.CharField("Стадия", choices=StageChoices.choices, max_length=32)
    profit = models.IntegerField(
        default=0, verbose_name="Профит", null=True, blank=True
    )
    required_founding = models.IntegerField(
        default=0, verbose_name="Требуемое финансирование", null=True, blank=True
    )
    already_distributed = models.IntegerField(
        default=0, verbose_name="Ранние вложения", null=True, blank=True
    )
    capital_offer = models.IntegerField(
        default=0, verbose_name="Предложение инвестору", null=True, blank=True
    )
    business_type = models.ManyToManyField(
        BusinessType, verbose_name="Тип бизнеса", blank=True, related_name="business"
    )
    development_stage = models.CharField(
        "Стадия разработки", choices=CurrentStage.choices, max_length=32
    )
    # purpose = models.ForeignKey(
    #     Purpose, models.SET_NULL, verbose_name="Цель", null=True, blank=True
    # )
    # business_model = models.CharField(
    #     "Бизнес модель",
    #     choices=BusinessTypes.choices,
    #     max_length=25,
    #     null=True,
    #     blank=True,
    # )
    # market_size = models.TextField(verbose_name="Размер рынка", null=True, blank=True)
    pitch_presentation = models.ForeignKey(
        File, models.SET_NULL, verbose_name="Файл презентации", null=True, blank=True
    )
    achievements = models.ForeignKey(
        Achievements,
        models.SET_NULL,
        verbose_name="Достижения",
        null=True,
        blank=True,
    )
    social_links = models.ForeignKey(
        Links, models.SET_NULL, verbose_name="Социальные сети", null=True, blank=True
    )

    detailed_description = models.TextField(
        verbose_name="Детальное описание", null=True, blank=True
    )
    work_team = models.ManyToManyField(
        # "vacancy.WorkTeam",
        WorkTeam,
        verbose_name="Команда",
        blank=True,
        related_name="startup_work_team",
    )

    # TODO : detailed_description под вопросом
    class Meta:
        verbose_name = "Стартап"
        verbose_name_plural = "Стартапы"

    def __str__(self):
        return f"{self.id} - {self.name}"
