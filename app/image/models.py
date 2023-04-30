from django.db import models

from versatileimagefield.fields import VersatileImageField, PPOIField

from image.validators import (
    validate_file_size,
    validate_file_extension,
    validate_image_extension,
    validate_image_size,
)


class Background(models.Model):
    background = VersatileImageField(
        "Background",
        upload_to="backgrounds/",
        ppoi_field="background_ppoi",
        validators=[validate_image_extension, validate_image_size],
    )
    background_ppoi = PPOIField()


class Logo(models.Model):
    logo = VersatileImageField(
        "Logo",
        upload_to="logos/",
        ppoi_field="logo_ppoi",
        validators=[validate_image_extension, validate_image_size],
    )
    logo_ppoi = PPOIField()


class File(models.Model):
    pdf = models.FileField(
        upload_to="pdf/", validators=[validate_file_size, validate_file_extension]
    )
