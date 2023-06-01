from .models import Image, File
from .serializers import ImageBaseSerializer, FileBaseSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import viewsets


class ImageViewSet(FlexFieldsModelViewSet):
    """Создание | Получение | Удаление изображения"""

    serializer_class = ImageBaseSerializer
    queryset = Image.objects.all()


class FilesViewSet(viewsets.ModelViewSet):
    """Создание | Получение | Удаление файла [.pdf, .pptx]"""

    queryset = File.objects.all()
    serializer_class = FileBaseSerializer
    # TODO : Валидация файлов
