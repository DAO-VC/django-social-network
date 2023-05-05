from django.urls import path

from articles.views import ArticleListCreateView, ArticleRetrieveView, ArticleParamView

urlpatterns = [
    path(
        "common/article/", ArticleListCreateView.as_view(), name="list_create_article"
    ),
    path("common/article/search/", ArticleParamView.as_view(), name="search_article"),
    path(
        "common/article/<int:pk>",
        ArticleRetrieveView.as_view(),
        name="retrieve_article",
    ),
]
