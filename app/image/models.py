from django.db import models

from versatileimagefield.fields import VersatileImageField, PPOIField

from image.validators import (
    validate_file_size,
    validate_file_extension,
    validate_image_extension,
    validate_image_size,
)


class Image(models.Model):
    image = VersatileImageField(
        "Background",
        upload_to="images/",
        ppoi_field="image_ppoi",
        validators=[validate_image_extension, validate_image_size],
    )
    image_ppoi = PPOIField()


# class Logo(models.Model):
#     logo = VersatileImageField(
#         "Logo",
#         upload_to="logos/",
#         ppoi_field="logo_ppoi",
#         validators=[validate_image_extension, validate_image_size],
#     )
#     logo_ppoi = PPOIField()


class File(models.Model):
    pdf = models.FileField(
        upload_to="files/", validators=[validate_file_size, validate_file_extension]
    )
