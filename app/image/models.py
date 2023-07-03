from django.db import models


class Image(models.Model):
    """Модель изображения"""

    image = models.FileField(
        "Background",
        upload_to="images/",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"{self.id} - Изображение"


class File(models.Model):
    """Модель файла"""

    pdf = models.FileField(upload_to="files/")

    class Meta:
        verbose_name = "Файл презентации"
        verbose_name_plural = "Файлы презентации"

    def __str__(self):
        return f"{self.id} - Документ"
