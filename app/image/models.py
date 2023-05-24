from django.db import models


class Image(models.Model):
    """Модель изображения"""

    image = models.FileField(
        "Background",
        upload_to="images/",
    )


class File(models.Model):
    """Модель файла"""

    pdf = models.FileField(upload_to="files/")
