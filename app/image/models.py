from django.db import models


class Image(models.Model):
    """Модель изображения"""

    image = models.FileField(
        "Background",
        upload_to="images/",
    )

    def __str__(self):
        return f"{self.id} - Изображение"


class File(models.Model):
    """Модель файла"""

    pdf = models.FileField(upload_to="files/")

    def __str__(self):
        return f"{self.id} - Документ"
