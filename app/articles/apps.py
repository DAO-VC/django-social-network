from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"
    verbose_name = "Блок Статьи"

    def ready(self) -> None:
        import articles.signals
