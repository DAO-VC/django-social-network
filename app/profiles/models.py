from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import User
from image.models import File, Image


class Startup(models.Model):
    """Модель сущности Стартап"""

    class StageChoices(models.TextChoices):
        SEED = "seed", "Основание"
        PRIVATE = "private", "Приват"
        STRATEGIC = "strategic", "Стратеджик"
        PUBLIC = "public", "Паблик"
        SECONDARY_FUNDRAISING = "secondaryFundraising", "Вторичное финансирование"
        NO_FUNDRAISING_REQUIRED = "noFundraisingRequired", "Финансирование не требуется"

    class BusinessType(models.TextChoices):
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

    # class CountryChoices(models.TextChoices):
    #     NORTHERN_AMERICA = "Northern America", "Северная Америка"
    #     CENTRAL_AMERICA_AND_CARIBBEAN = (
    #         "Central America & Caribbean",
    #         "Центральная Америка и Карибы",
    #     )
    #     SOUTH_AMERICA = "South America", "Южная Америка"
    #     NORDICS_AND_BALTICS = "Nordics & Baltics", "Северо-Балтийск"
    #     WESTERN_EUROPE = "Western Europe", "Западная Европа"
    #     SOUTHERN_EUROPE = "Southern Europe", "Южная Европа"
    #     EASTERN_EUROPE_AND_RUSSIA = (
    #         "Eastern Europe & Russia",
    #         "Восточная Европа и Россия",
    #     )
    #     NORTHERN_AFRICA_AND_MIDDLE_EAST = (
    #         "Northern Africa & Middle East",
    #         "Северная Африка и Ближний Восток",
    #     )
    #     AFRICA = "Africa", "Африка"
    #     ASIA = "Asia", "Азия"
    #     WORLDWIDE = "Worldwide", "Мировой"
    #     AUSTRALIA_NEW_ZEALAND_OCEANIA = (
    #         "Australia, New Zealand & Oceania",
    #         "Австралия, Новая зеландия и Океания",
    #     )

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField("Название", max_length=32)
    url = models.TextField("Урл", null=True, blank=True)
    foundation_year = models.IntegerField(null=True, blank=True)
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
        "Industries", verbose_name="Индустрии", blank=True, related_name="industries"
    )
    is_registered = models.BooleanField(verbose_name="Уже зарегистрирована")

    registration_country = models.ForeignKey(
        "SaleRegions",
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
        "SaleRegions",
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
        "BusinessType", verbose_name="Тип бизнеса", blank=True, related_name="business"
    )
    development_stage = models.CharField(
        "Стадия разработки", choices=CurrentStage.choices, max_length=32
    )
    purpose = models.ForeignKey(
        "Purpose", models.SET_NULL, verbose_name="Цель", null=True, blank=True
    )
    business_model = models.CharField(
        "Бизнес модель",
        choices=BusinessType.choices,
        max_length=25,
        null=True,
        blank=True,
    )
    market_size = models.TextField(verbose_name="Размер рынка", null=True, blank=True)
    pitch_presentation = models.ForeignKey(
        File, models.CASCADE, verbose_name="Файл презентации", null=True, blank=True
    )
    achievements = models.ForeignKey(
        "Achievements",
        models.SET_NULL,
        verbose_name="Достижения",
        null=True,
        blank=True,
    )
    social_links = models.ForeignKey(
        "Links", models.SET_NULL, verbose_name="Социальные сети", null=True, blank=True
    )

    detailed_description = models.TextField(
        verbose_name="Детальное описание", null=True, blank=True
    )
    work_team = models.ManyToManyField(
        "vacancy.WorkTeam",
        verbose_name="Команда",
        blank=True,
        related_name="startup_work_team",
    )

    # TODO : detailed_description под вопросом
    class Meta:
        verbose_name = "Стартап"
        verbose_name_plural = "Стартапы"


class Investor(models.Model):
    """Модель сущности инвестор"""

    owner = models.ForeignKey(User, models.CASCADE)
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
        "Industries",
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
        return self.name


class Professional(models.Model):
    """Модель сущности профессионал"""

    owner = models.ForeignKey(User, models.CASCADE)
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
    cv = models.ForeignKey(
        File, models.SET_NULL, verbose_name="Файл презентации", null=True, blank=True
    )

    # TODO: вопрос о формате файла ( они разные в стартапе и здесь)
    # TODO: Добавить интересы
    speciality = models.CharField("Специальность", max_length=32, null=True, blank=True)
    skills = models.ManyToManyField(
        "Industries", verbose_name="Скилы", blank=True, related_name="skills"
    )
    # interest = models.ManyToManyField(
    #     "Industries", verbose_name="Интересы", blank=True, related_name="prof_interest"
    # )
    salary = models.TextField(verbose_name="Зарплата", null=True, blank=True)

    class Meta:
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"

    def __str__(self):
        return self.name


class Industries(models.Model):
    """Модель индустрии"""

    class IndustriesType(models.TextChoices):
        BLOCKCHAIN = "blockchain", "Блокчейн"
        OTHER = "other", "Остальное"

    title = models.CharField("Название", max_length=50)
    type = models.CharField(choices=IndustriesType.choices, max_length=25)

    def __str__(self):
        return self.title


class Achievements(models.Model):
    """Модель достижения"""

    accelerator = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    conference = models.TextField(verbose_name="Конференция", null=True, blank=True)
    hackathon = models.TextField(verbose_name="Хакатон", null=True, blank=True)
    mass_media = models.TextField(verbose_name="Массмедиа", null=True, blank=True)
    awards = models.TextField(verbose_name="Награды", null=True, blank=True)
    other = models.TextField(verbose_name="Другое", null=True, blank=True)


class Purpose(models.Model):
    """Модель цель"""

    problem = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    decision = models.TextField(verbose_name="Конференция", null=True, blank=True)


class Links(models.Model):
    """Модель социальные сети"""

    app_store = models.TextField("Аппстор", null=True, blank=True)
    google_play = models.TextField("Гуглплэй", null=True, blank=True)
    twitter = models.TextField("Твиттер", null=True, blank=True)
    telegram = models.TextField("Телеграм", null=True, blank=True)
    youtube = models.TextField("Ютуб", null=True, blank=True)
    discord = models.TextField("Дискорд", null=True, blank=True)
    facebook = models.TextField("Фэйсбук", null=True, blank=True)
    instagram = models.TextField("Инстаграм", null=True, blank=True)
    linkedin = models.TextField("Линкедин", null=True, blank=True)
    medium = models.TextField("Медиум", null=True, blank=True)


class SaleRegions(models.Model):
    """Модель регионы продажи"""

    name = models.CharField("Название", max_length=32)

    def __str__(self):
        return self.name


class BusinessType(models.Model):
    """Модель бизнес типы"""

    title = models.CharField("Название", max_length=32)
    full_title = models.CharField("Полное название", max_length=32)
    description = models.TextField("Описание")

    def __str__(self):
        return self.title


# class Resume(models.Model):
#     professional_id = models.ForeignKey(Professional, models.CASCADE)
#     link = models.CharField("Ссылка", max_length=32, null=True, blank=True)
#     name_surname = models.CharField("Имя-фамилия", max_length=32)
#     position = models.CharField("Позиция", max_length=32)
#     phone = PhoneNumberField(max_length=128, verbose_name="Номер телефона")
#     email = models.EmailField("Email адрес")
#     salary = models.IntegerField(verbose_name="Зарплата")
#     about = models.TextField(verbose_name="Обо мне", null=True, blank=True)
#     education = models.TextField(verbose_name="Образование", null=True, blank=True)
#     work_experience = models.TextField(
#         verbose_name="Опыт работы", null=True, blank=True
#     )
#     skills = models.ManyToManyField(
#         Industries, verbose_name="Скилы", blank=True, related_name="resume_skills"
#     )
#     photo = models.ForeignKey(
#         Image, models.CASCADE, verbose_name="Фото", null=True, blank=True
#     )
#     cv = models.ForeignKey(
#         File, models.CASCADE, verbose_name="Файл презентации", null=True, blank=True
#     )
#
#     def __str__(self):
#         return self.name_surname
