from django.db import transaction
from rest_framework import serializers

from articles.models import Article
from image.serializers import ImageSerializer
from profiles.models import Startup
from django.db.models import Q


class ArticleBaseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__id__in=[
                    self.context["request"].user.id
                ]
            )
            | Q(owner=self.context["request"].user)
        ).first()
        with transaction.atomic():
            article = Article.objects.create(**validated_data, company_id=company_id)
        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Article
        fields = "__all__"


class ArticleUpdateVisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["company_id", "image", "name", "description", "is_visible"]

    def update(self, instance: Article, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True

        instance.save()
        return instance
