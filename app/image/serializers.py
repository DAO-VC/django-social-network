from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from main import settings
from .models import Image, File
from versatileimagefield.serializers import VersatileImageFieldSerializer


# class ImageSerializer(FlexFieldsModelSerializer):
#     image = VersatileImageFieldSerializer(sizes="product_headshot")
#
#     class Meta:
#         model = Image
#         fields = [
#             "id",
#             "image",
#         ]


# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = [
#             "id",
#             "image",
#         ]
class ImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "image", "name"]

    def get_image(self, value):
        # Build absolute URL (next line is just sample code)
        url = f"http://social-dev.dao.vc{settings.MEDIA_URL}{str(value.image)}"
        return url

    def get_name(self, value):
        return f"{str(value.image).split('/')[1]}"


class FileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ["id", "pdf", "name"]

    def get_pdf(self, value):
        # Build absolute URL (next line is just sample code)
        url = f"http://social-dev.dao.vc{settings.MEDIA_URL}{str(value.pdf)}"
        return url

    def get_name(self, value):
        return f"{str(value.pdf).split('/')[1]}"
