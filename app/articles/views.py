from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from articles.filters import ArticleFilter
from articles.models import Article
from articles.permissions import ArticlePermission, ArticleBasePermission
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
    ArticleBaseSerializer,
    ArticleUpdateVisionSerializer,
)

from django.db.models import F, Q


class ArticleListCreateView(generics.ListCreateAPIView):
    """Список всех постов стартапа | создание поста"""

    permission_classes = (IsAuthenticated, ArticleBasePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleCreateSerializer

    def get_queryset(self):
        obj = Article.objects.filter(
            Q(
                company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(company_id__owner=self.request.user.id)
        )
        self.check_object_permissions(self.request, obj)
        return obj


class ArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление поста"""

    queryset = Article.objects.all()
    http_method_names = ["get", "put", "delete"]
    permission_classes = (IsAuthenticated, ArticlePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleUpdateSerializer


class ArticleParamView(generics.ListAPIView):
    """Список всех статей | Поиск по названию поста"""

    serializer_class = ArticleBaseSerializer
    filterset_class = ArticleFilter

    def get_queryset(self):
        return Article.objects.filter(is_visible=True)


class ArticleVisibleView(generics.UpdateAPIView):
    """Обновление видимости статьи стартапом"""

    serializer_class = ArticleUpdateVisionSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, ArticlePermission)

    def get_queryset(self):
        return Article.objects.filter(
            Q(
                company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(company_id__owner=self.request.user.id)
        )


class AllArticleRetrieveView(generics.RetrieveAPIView):
    """Список всех статей по id"""

    serializer_class = ArticleBaseSerializer
    filterset_class = ArticleFilter

    def get_queryset(self):
        return Article.objects.filter(is_visible=True)

    def retrieve(self, request, *args, **kwargs):
        instance: Article = self.get_object()
        instance.view_count = F("view_count") + 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)
