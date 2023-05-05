from .models import Background, Logo, File
from .serializers import BackgroundSerializer, LogoSerializer, FileSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import viewsets


class BackgroundViewSet(FlexFieldsModelViewSet):
    """Создание | Получение | Удаление бэкграунда"""

    serializer_class = BackgroundSerializer
    queryset = Background.objects.all()


class LogoViewSet(FlexFieldsModelViewSet):
    """Создание | Получение | Удаление лого"""

    serializer_class = LogoSerializer
    queryset = Logo.objects.all()


class FilesViewSet(viewsets.ModelViewSet):
    """Создание | Получение | Удаление файла [.pdf, .pptx]"""

    queryset = File.objects.all()
    serializer_class = FileSerializer
    # TODO : Валидация файлов
