from django_filters import rest_framework

from articles.models import Article


class ArticleFilter(rest_framework.FilterSet):
    class Meta:
        model = Article
        fields = {
            "name": ("exact",),
        }

    # TODO : изменить на базовую фильтрацию
