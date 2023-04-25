from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import Background, Logo, File
from versatileimagefield.serializers import VersatileImageFieldSerializer


class BackgroundSerializer(FlexFieldsModelSerializer):
    background = VersatileImageFieldSerializer(sizes="product_headshot")

    class Meta:
        model = Background
        fields = [
            "id",
            "background",
        ]


class LogoSerializer(FlexFieldsModelSerializer):
    logo = VersatileImageFieldSerializer(sizes="product_headshot")

    class Meta:
        model = Logo
        fields = [
            "id",
            "logo",
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "pdf",
        ]
