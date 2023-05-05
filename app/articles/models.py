from django.db import models

from image.models import Logo
from profiles.models import Startup


class Article(models.Model):
    company_id = models.ForeignKey(Startup, models.CASCADE)
    name = models.CharField("Заголовок", max_length=32)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ForeignKey(
        Logo, models.CASCADE, verbose_name="Фото", null=True, blank=True
    )
    # TODO : tags ??
    # TODO: обязательные поля

    def __str__(self):
        return self.name
