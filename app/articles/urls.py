from django.urls import path

from articles.views import (
    ArticleListCreateView,
    ArticleRetrieveView,
    ArticleParamView,
)

urlpatterns = [
    path("main/article/", ArticleListCreateView.as_view(), name="list_create_article"),
    path("common/articles/", ArticleParamView.as_view(), name="all_articles"),
    path(
        "main/article/<int:pk>",
        ArticleRetrieveView.as_view(),
        name="retrieve_article",
    ),
    # path("main/articles/", AllArticleListView.as_view(), name="all_list_article"),
]
