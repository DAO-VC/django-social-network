from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profiles.models import Startup
from vacancy.models import Vacancy


class VacancyCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(owner=self.context["request"].user).first()
        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("Минимум один скил")

        vacancy = Vacancy.objects.create(**validated_data, company_id=company_id)
        vacancy.skills.set(skills)

        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Vacancy
        fields = "__all__"

    def update(self, instance, validated_data):

        skills = validated_data.pop("skills")
        if len(skills) > 0:
            instance.skills.set(skills)

        return super().update(instance, validated_data)
