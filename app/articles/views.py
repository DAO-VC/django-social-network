from django.shortcuts import render
from rest_framework import generics

from articles.models import Article
from articles.serializers import ArticleCreateSerializer, ArticleUpdateSerializer


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
