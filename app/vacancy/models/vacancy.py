from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from profiles.models.other_models import Industries


class Vacancy(models.Model):
    """Сущность вакансии стартапа"""

    company_id = models.ForeignKey("profiles.Startup", models.CASCADE)
    position = models.CharField("Позиция", max_length=32)
    requirements = models.CharField("Требования", max_length=32)
    is_visible = models.BooleanField(verbose_name="Активен")
    salary = models.IntegerField(verbose_name="Зарплата")
    skills = models.ManyToManyField(
        Industries, verbose_name="Скилы", blank=True, related_name="vacancy_skills"
    )
    created_at = CreationDateTimeField(verbose_name="Дата создания")
    # TODO: обязательные поля
