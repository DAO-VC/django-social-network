from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import User
from image.models import File, Logo, Background


class Startup(models.Model):
    """Модель сущности Стартап"""

    class StageChoices(models.TextChoices):
        ANGEL = "Angel", "Ангел"
        PRE_SEED = "Pre-Seed", "Пресид"
        SEED = "Seed", "Сид"

    class BusinessType(models.TextChoices):
        B2B = "B2B", "Business to Business"
        B2C = "B2C", "Business to consumer"
        B2G = "B2G", "Business to Government"
        C2B = "C2B", "Consumer to business"
        C2C = "C2C", "Consumer to consumer"
        C2G = "C2G", "Consumer to Government"
        SAAS = "SAAS", "Software on Demand"

    class CurrentStage(models.TextChoices):
        PROJECT_START = "Project Start", "Старт проекта"
        WORKING_ON_THE_PRODUCT = "Working on the product", "Работа над продуктом"
        ENTERING_THE_MARKET = "Entering the market", "Выход на рынок"
        GROWTH_AND_SCALING = "Growth and scaling", "Рост и масштабирование"

    class CountryChoices(models.TextChoices):
        NORTHERN_AMERICA = "Northern America", "Северная Америка"
        CENTRAL_AMERICA_AND_CARIBBEAN = (
            "Central America & Caribbean",
            "Центральная Америка и Карибы",
        )
        SOUTH_AMERICA = "South America", "Южная Америка"
        NORDICS_AND_BALTICS = "Nordics & Baltics", "Северо-Балтийск"
        WESTERN_EUROPE = "Western Europe", "Западная Европа"
        SOUTHERN_EUROPE = "Southern Europe", "Южная Европа"
        EASTERN_EUROPE_AND_RUSSIA = (
            "Eastern Europe & Russia",
            "Восточная Европа и Россия",
        )
        NORTHERN_AFRICA_AND_MIDDLE_EAST = (
            "Northern Africa & Middle East",
            "Северная Африка и Ближний Восток",
        )
        AFRICA = "Africa", "Африка"
        ASIA = "Asia", "Азия"
        WORLDWIDE = "Worldwide", "Мировой"
        AUSTRALIA_NEW_ZEALAND_OCEANIA = (
            "Australia, New Zealand & Oceania",
            "Австралия, Новая зеландия и Океания",
        )

    owner = models.ForeignKey(User, models.PROTECT)
    name = models.CharField("Название", max_length=32)
    url = models.CharField("Урл", max_length=32, null=True, blank=True)
    foundation_year = models.IntegerField(null=True, blank=True)
    short_description = models.TextField(verbose_name="Описание", null=True, blank=True)
    logo = models.ForeignKey(Logo, models.CASCADE, verbose_name="Логотип")
    background = models.ForeignKey(Background, models.CASCADE, verbose_name="Бэкграунд")
    industries = models.ManyToManyField(
        "Industries", verbose_name="Индустрии", blank=True, related_name="industries"
    )
    is_registered = models.BooleanField(verbose_name="Уже зарегистрирована")

    registration_country = models.CharField(
        "Статус", choices=CountryChoices.choices, max_length=50
    )
    headquartered = models.CharField("Штаб-квартира", max_length=32)
    regions = models.ManyToManyField(
        "SaleRegions",
        verbose_name="Регионы продажи",
        blank=True,
        related_name="industries",
    )
    stage = models.CharField("Стадия", choices=StageChoices.choices, max_length=10)
    profit = models.IntegerField(default=0, verbose_name="Профит")
    required_founding = models.IntegerField(
        default=0, verbose_name="Требуемое финансирование"
    )
    already_distributed = models.IntegerField(default=0, verbose_name="Ранние вложения")
    capital_offer = models.IntegerField(default=0, verbose_name="Предложение инвестору")
    business_type = models.ManyToManyField(
        "BusinessType", verbose_name="Тип бизнеса", blank=True, related_name="business"
    )
    development_stage = models.CharField(
        "Стадия разработки", choices=CurrentStage.choices, max_length=32
    )
    purpose = models.ForeignKey("Purpose", models.CASCADE, verbose_name="Цель")
    business_model = models.CharField(
        "Бизнес модель", choices=BusinessType.choices, max_length=25
    )
    market_size = models.TextField(verbose_name="Размер рынка")
    pitch_presentation = models.ForeignKey(
        File, models.CASCADE, verbose_name="Файл презентации"
    )
    achievements = models.ForeignKey(
        "Achievements", models.CASCADE, verbose_name="Достижения"
    )
    social_links = models.ForeignKey(
        "Links", models.CASCADE, verbose_name="Социальные сети"
    )

    detailed_description = models.TextField(verbose_name="Детальное описание")

    # TODO : detailed_description под вопросом
    class Meta:
        verbose_name = "Стартап"
        verbose_name_plural = "Стартапы"


class Investor(models.Model):
    owner = models.ForeignKey(User, models.PROTECT)
    name = models.CharField("Имя", max_length=32)
    lastName = models.CharField("Фамилия", max_length=32)
    phone = PhoneNumberField(max_length=128, verbose_name="Номер телефона")
    about = models.TextField(verbose_name="Обо мне")
    photo = models.ForeignKey(Logo, models.CASCADE, verbose_name="Фото")
    interest = models.ManyToManyField(
        "Industries",
        verbose_name="Интересы",
        blank=True,
        related_name="invest_interest",
    )
    cv = models.ForeignKey(File, models.CASCADE, verbose_name="Файл презентации")

    class Meta:
        verbose_name = "Инвестор"
        verbose_name_plural = "Инвесторы"

    def __str__(self):
        return self.name


class Professional(models.Model):
    owner = models.ForeignKey(User, models.PROTECT)
    name = models.CharField("Имя", max_length=32)
    lastName = models.CharField("Фамилия", max_length=32)
    email = models.EmailField("Email адрес")
    phone = PhoneNumberField(max_length=128, verbose_name="Номер телефона")
    about = models.TextField(verbose_name="Обо мне")
    photo = models.ForeignKey(Logo, models.CASCADE, verbose_name="Фото")
    cv = models.ForeignKey(File, models.CASCADE, verbose_name="Файл презентации")

    # TODO: вопрос о формате файла ( они разные в стартапе и здесь)
    # TODO: Добавить интересы
    skills = models.ManyToManyField(
        "Industries", verbose_name="Скилы", blank=True, related_name="skills"
    )
    interest = models.ManyToManyField(
        "Industries", verbose_name="Интересы", blank=True, related_name="prof_interest"
    )
    salary = models.TextField(verbose_name="Зарплата")

    class Meta:
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"

    def __str__(self):
        return self.name


class Industries(models.Model):
    class IndustriesType(models.TextChoices):
        BLOCKCHAIN = "blockchain", "Блокчейн"
        OTHER = "other", "Остальное"

    title = models.CharField("Название", max_length=50)
    type = models.CharField(choices=IndustriesType.choices, max_length=25)

    def __str__(self):
        return self.title


class Achievements(models.Model):
    accelerator = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    conference = models.TextField(verbose_name="Конференция", null=True, blank=True)
    hackathon = models.TextField(verbose_name="Хакатон", null=True, blank=True)
    mass_media = models.TextField(verbose_name="Массмедиа", null=True, blank=True)
    awards = models.TextField(verbose_name="Награды", null=True, blank=True)
    other = models.TextField(verbose_name="Другое", null=True, blank=True)


class Purpose(models.Model):
    problem = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    decision = models.TextField(verbose_name="Конференция", null=True, blank=True)


class Links(models.Model):
    app_store = models.CharField("Аппстор", max_length=32, null=True, blank=True)
    google_play = models.CharField("Гуглплэй", max_length=32, null=True, blank=True)
    twitter = models.CharField("Твиттер", max_length=32, null=True, blank=True)
    telegram = models.CharField("Телеграм", max_length=32, null=True, blank=True)
    youtube = models.CharField("Ютуб", max_length=32, null=True, blank=True)
    discord = models.CharField("Дискорд", max_length=32, null=True, blank=True)
    facebook = models.CharField("Фэйсбук", max_length=32, null=True, blank=True)
    instagram = models.CharField("Инстаграм", max_length=32, null=True, blank=True)
    linkedin = models.CharField("Линкедин", max_length=32, null=True, blank=True)
    medium = models.CharField("Медиум", max_length=32, null=True, blank=True)


class SaleRegions(models.Model):
    name = models.CharField("Название", max_length=32)

    def __str__(self):
        return self.name


class BusinessType(models.Model):
    title = models.CharField("Название", max_length=32)

    def __str__(self):
        return self.title
