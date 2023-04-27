from .models import Background, Logo, File
from .serializers import BackgroundSerializer, LogoSerializer, FileSerializer
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework import viewsets


class BackgroundViewSet(FlexFieldsModelViewSet):
    serializer_class = BackgroundSerializer
    queryset = Background.objects.all()


class LogoViewSet(FlexFieldsModelViewSet):
    serializer_class = LogoSerializer
    queryset = Logo.objects.all()


class FilesViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # TODO : Валидация файлов
