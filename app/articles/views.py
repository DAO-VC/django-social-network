from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from articles.filters import ArticleFilter
from articles.models import Article
from articles.permissions import ArticlePermission
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
    ArticleBaseSerializer,
)
from core.permissions import StartupCreatePermission


class AllArticleListView(generics.ListAPIView):
    """Список всех постов сайта"""

    queryset = Article.objects.all()
    serializer_class = ArticleBaseSerializer
    # TODO: сортировка по дате создания


class ArticleListCreateView(generics.ListCreateAPIView):
    """Список всех постов стартапа | создание поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleCreateSerializer

    def get_queryset(self):
        return Article.objects.filter(company_id__owner_id=self.request.user.id)


class ArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = (IsAuthenticated, ArticlePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleBaseSerializer
        return ArticleUpdateSerializer


class ArticleParamView(generics.ListAPIView):
    """Поиск по названию поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleBaseSerializer
    filterset_class = ArticleFilter
    permission_classes = (IsAuthenticated,)
