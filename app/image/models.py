from django.db import models
from image.validators import (
    validate_file_size,
    validate_image_size,
)


class Image(models.Model):
    image = models.FileField(
        "Background",
        upload_to="images/",
        validators=[validate_image_size],
    )


class File(models.Model):
    pdf = models.FileField(upload_to="files/", validators=[validate_file_size])
