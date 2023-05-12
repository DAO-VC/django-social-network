from django.db import models

from versatileimagefield.fields import VersatileImageField, PPOIField

from image.validators import (
    validate_file_size,
    validate_file_extension,
    validate_image_extension,
    validate_image_size,
)


# class Image(models.Model):
#     image = VersatileImageField(
#         "Background",
#         upload_to="images/",
#         ppoi_field="image_ppoi",
#         validators=[validate_image_extension, validate_image_size],
#     )
#     image_ppoi = PPOIField()


class Image(models.Model):
    image = models.FileField(
        "Background",
        upload_to="images/",
        validators=[validate_image_size],
    )


class File(models.Model):
    pdf = models.FileField(upload_to="files/", validators=[validate_file_size])
