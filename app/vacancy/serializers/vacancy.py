from django.db import transaction
from rest_framework import serializers
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from profiles.models.startup import Startup
from vacancy.models.vacancy import Vacancy


class VacancyBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор вакансии"""

    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCreateSerializer(serializers.ModelSerializer):
    """Сериализато создания вакансии"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__in=[
                    self.context["request"].user.id
                ]
            )
            | Q(owner=self.context["request"].user)
        ).first()

        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("Минимум один скил")
        with transaction.atomic():
            vacancy = Vacancy.objects.create(**validated_data, company_id=company_id)
            vacancy.skills.set(skills)

        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления вакансии"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def update(self, instance, validated_data):
        skills = validated_data.pop("skills")
        if len(skills) > 0:
            instance.skills.set(skills)

        return super().update(instance, validated_data)


class VacancyVisibleSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости вакансии"""

    class Meta:
        model = Vacancy
        fields = "__all__"
        read_only_fields = (
            "company_id",
            "position",
            "salary",
            "salary_type",
            "work_schedude",
            "place",
            "skills",
            "description",
            "requirements",
            "is_visible",
            "created_at",
        )

    def update(self, instance: Vacancy, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True
        instance.save()
        return instance
