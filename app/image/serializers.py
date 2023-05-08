from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from .models import Image, File
from versatileimagefield.serializers import VersatileImageFieldSerializer


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(sizes="product_headshot")

    class Meta:
        model = Image
        fields = [
            "id",
            "image",
        ]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "pdf",
        ]
