from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from image.tasks import cleaner, cleaner_file
from image.serializers import ImageSerializer, FileSerializer
from profiles.models.professional import Professional


class ProfessionalBaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания профессионала"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Professional
        fields = "__all__"

    def create(self, validated_data):
        skills = validated_data.pop("skills")
        if len(skills) < 1:
            raise ValidationError("skills : minimum  one skill")
        # interest = validated_data.pop("interest")
        # if len(skills) < 1:
        #     raise ValidationError("interest : minimum  one interest")
        owner = self.context["request"].user
        with transaction.atomic():
            professional = Professional.objects.create(**validated_data, owner=owner)

            professional.skills.set(skills)
            # professional.interest.set(interest)

            owner.is_onboarding = True
            owner.save()

        return professional


class ProfessionalUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения профессионала"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Professional
        fields = "__all__"

    def update(self, instance: Professional, validated_data):
        skills = validated_data.pop("skills")
        if len(skills) > 0:
            instance.skills.set(skills)

        # interest = validated_data.pop("interest")
        # if len(interest) > 0:
        #     instance.interest.set(interest)
        if instance.photo:
            object_photo_id = instance.photo.id
            new_photo_id = validated_data.get("photo")
            if new_photo_id:
                new_photo_id = new_photo_id.id

            cleaner.delay(object_photo_id, new_photo_id)

        if instance.cv:
            object_cv_id = instance.cv.id
            new_cv_id = validated_data.get("cv")
            if new_cv_id:
                new_cv_id = new_cv_id.id

            cleaner_file.delay(object_cv_id, new_cv_id)

        return super().update(instance, validated_data)


class ProfessionalSerializer(serializers.ModelSerializer):
    """Базовый сериализатор профессионала"""

    photo = ImageSerializer(read_only=True)
    cv = FileSerializer(read_only=True)

    class Meta:
        model = Professional
        fields = "__all__"
