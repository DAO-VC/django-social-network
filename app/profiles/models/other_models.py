from django.db import models


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
