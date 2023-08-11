from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from image.tasks import cleaner, cleaner_file
from image.serializers import ImageSerializer, FileSerializer
from profiles.models.investor import Investor
from profiles.models.other_models import Links
from profiles.serializers.others_serializers import LinkSerializer


class InvestorBaseSerializer(serializers.ModelSerializer):
    """Сериализатор создания инвестора"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"

    def create(self, validated_data):
        interest = validated_data.pop("interest")
        if len(interest) < 1:
            raise ValidationError("Минимум одна индустрия")
        owner = self.context["request"].user
        social_links = validated_data.pop("social_links")
        social_links_obj = Links.objects.create(**social_links)
        with transaction.atomic():
            investor = Investor.objects.create(
                **validated_data, owner=owner, social_links=social_links_obj
            )

            investor.interest.set(interest)

            owner.is_onboarding = True
            owner.save()

        return investor


class InvestorUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения инвестора"""

    owner = serializers.SlugRelatedField(read_only=True, slug_field="id")
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"

    def update(self, instance, validated_data):
        interest = validated_data.pop("interest")
        if len(interest) > 0:
            instance.interest.set(interest)

        if "social_links" in validated_data:
            social_links_serializer = self.fields["social_links"]
            social_links_instance = instance.social_links
            social_links_data = validated_data.pop("social_links")
            social_links_serializer.update(social_links_instance, social_links_data)

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


class InvestorSerializer(serializers.ModelSerializer):
    """Базовый сериализатор инвестора"""

    photo = ImageSerializer(read_only=True)
    cv = FileSerializer(read_only=True)
    social_links = LinkSerializer()

    class Meta:
        model = Investor
        fields = "__all__"


class InvestorChatSerializer(serializers.ModelSerializer):
    photo = ImageSerializer(read_only=True)

    class Meta:
        model = Investor
        fields = ["id", "owner", "name", "photo"]
