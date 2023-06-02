from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from core.models import User
from image.models import Image, File
from profiles.models.other_models import Industries


class Professional(models.Model):
    """Модель сущности профессионал"""

    owner = models.ForeignKey(User, models.CASCADE)
    name = models.CharField("Имя", max_length=32)
    lastName = models.CharField("Фамилия", max_length=32)
    email = models.EmailField("Email адрес")
    phone = PhoneNumberField(
        max_length=128, verbose_name="Номер телефона", null=True, blank=True
    )
    about = models.TextField(verbose_name="Обо мне", null=True, blank=True)
    photo = models.ForeignKey(
        Image, models.SET_NULL, verbose_name="Фото", null=True, blank=True
    )
    cv = models.ForeignKey(
        File, models.SET_NULL, verbose_name="Файл презентации", null=True, blank=True
    )

    # TODO: вопрос о формате файла (они разные в стартапе и здесь)
    # TODO: Добавить интересы
    speciality = models.CharField("Специальность", max_length=32, null=True, blank=True)
    skills = models.ManyToManyField(
        Industries, verbose_name="Скилы", blank=True, related_name="skills"
    )
    # interest = models.ManyToManyField(
    #     "Industries", verbose_name="Интересы", blank=True, related_name="prof_interest"
    # )
    salary = models.TextField(verbose_name="Зарплата", null=True, blank=True)

    class Meta:
        verbose_name = "Профессионал"
        verbose_name_plural = "Профессионалы"

    def __str__(self):
        return self.name
