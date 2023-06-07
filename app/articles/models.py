from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from image.models import Image
from profiles.models.startup import Startup


class Article(models.Model):
    """Сущность статьи стартапа"""

    company_id = models.ForeignKey(Startup, models.CASCADE)
    name = models.CharField("Заголовок", max_length=32)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ForeignKey(
        Image, models.SET_NULL, verbose_name="Фото", null=True, blank=True
    )
    is_visible = models.BooleanField(verbose_name="Видим")
    view_count = models.IntegerField(default=0, null=True, blank=True)
    created_at = CreationDateTimeField(verbose_name="Дата создания")
    tags = models.ManyToManyField("Tag", related_name="article_tags", blank=True)

    # TODO заменить поле на CreationDateTimeField из django-extensions
    # TODO : tags ??
    # TODO: обязательные поля

    def __str__(self):
        return self.name

    def change_visible(self):
        if self.is_visible:
            self.is_visible = False
        else:
            self.is_visible = True


class Tag(models.Model):
    title = models.CharField("Заголовок", max_length=32)

    def __str__(self):
        return self.title
