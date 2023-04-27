from django.db import models

from versatileimagefield.fields import VersatileImageField, PPOIField


class Background(models.Model):
    background = VersatileImageField(
        "Background", upload_to="backgrounds/", ppoi_field="background_ppoi"
    )
    background_ppoi = PPOIField()


class Logo(models.Model):
    logo = VersatileImageField("Logo", upload_to="logos/", ppoi_field="logo_ppoi")
    logo_ppoi = PPOIField()


class File(models.Model):
    pdf = models.FileField(upload_to="pdf/")
