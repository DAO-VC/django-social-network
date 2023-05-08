from .models import Image, File
from .serializers import ImageSerializer, FileSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import viewsets


class ImageViewSet(FlexFieldsModelViewSet):
    """Создание | Получение | Удаление изображения"""

    serializer_class = ImageSerializer
    queryset = Image.objects.all()


# class LogoViewSet(FlexFieldsModelViewSet):
#     """Создание | Получение | Удаление лого"""
#
#     serializer_class = LogoSerializer
#     queryset = Logo.objects.all()


class FilesViewSet(viewsets.ModelViewSet):
    """Создание | Получение | Удаление файла [.pdf, .pptx]"""

    queryset = File.objects.all()
    serializer_class = FileSerializer
    # TODO : Валидация файлов
