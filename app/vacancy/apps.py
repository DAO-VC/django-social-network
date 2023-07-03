from django.apps import AppConfig


class VacancyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vacancy"
    verbose_name = "Блок Вакансии"

    def ready(self) -> None:
        import vacancy.signals
