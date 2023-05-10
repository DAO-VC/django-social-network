from django.shortcuts import render
from rest_framework import generics

from articles.filters import ArticleFilter
from articles.models import Article
from articles.serializers import ArticleCreateSerializer, ArticleUpdateSerializer


class AllArticleListView(generics.ListAPIView):
    """Список всех постов сайта"""

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    # TODO: сортировка по дате создания


class ArticleListCreateView(generics.ListCreateAPIView):
    """Список всех постов стартапа | создание поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer

    def get_queryset(self):
        return Article.objects.filter(company_id__owner_id=self.request.user.id)


class ArticleRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    http_method_names = ["get", "put", "delete"]


class ArticleParamView(generics.ListAPIView):
    """Поиск по названию поста"""

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    filterset_class = ArticleFilter
