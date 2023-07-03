from django.db import models


class Industries(models.Model):
    """Модель индустрии"""

    class IndustriesType(models.TextChoices):
        BLOCKCHAIN = "blockchain", "Блокчейн"
        OTHER = "other", "Остальное"

    title = models.CharField("Название", max_length=50)
    type = models.CharField(choices=IndustriesType.choices, max_length=25)

    class Meta:
        verbose_name = "Индустрия"
        verbose_name_plural = "Индустрии"

    def __str__(self):
        return f"{self.id} -  {self.title}"


class Achievements(models.Model):
    """Модель достижения"""

    accelerator = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    conference = models.TextField(verbose_name="Конференция", null=True, blank=True)
    hackathon = models.TextField(verbose_name="Хакатон", null=True, blank=True)
    mass_media = models.TextField(verbose_name="Массмедиа", null=True, blank=True)
    awards = models.TextField(verbose_name="Награды", null=True, blank=True)
    other = models.TextField(verbose_name="Другое", null=True, blank=True)

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

    def __str__(self):
        return f"{self.id} - Достижение"


class Purpose(models.Model):
    """Модель цель"""

    problem = models.TextField(verbose_name="Акселератор", null=True, blank=True)
    decision = models.TextField(verbose_name="Конференция", null=True, blank=True)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return f"{self.id} - Цель"


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

    class Meta:
        verbose_name = "Url"
        verbose_name_plural = "Urls"

    def __str__(self):
        return f"{self.id} - Urls"


class SaleRegions(models.Model):
    """Модель регионы продажи"""

    name = models.CharField("Название", max_length=32)

    class Meta:
        verbose_name = "Регион продаж"
        verbose_name_plural = "Регионы продаж"

    def __str__(self):
        return f"{self.id} - {self.name}"


class BusinessType(models.Model):
    """Модель бизнес типы"""

    title = models.CharField("Название", max_length=32)
    full_title = models.CharField("Полное название", max_length=32)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Бизнес тип"
        verbose_name_plural = "Бизнес типы"

    def __str__(self):
        return f"{self.id} - {self.title}"
