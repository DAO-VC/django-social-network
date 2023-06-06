from django.db import transaction
from rest_framework import serializers
from articles.models import Article, Tag
from image.serializers import ImageSerializer
from django.db.models import Q

from profiles.models.startup import Startup


class ArticleBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор статьи"""

    image = ImageSerializer(read_only=True)
    is_visible = serializers.BooleanField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания статьи"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    tags = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)
    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=30), write_only=True
    )
    view_count = serializers.IntegerField(read_only=True)
    is_visible = serializers.BooleanField(read_only=True)

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
        tag_titles = validated_data.pop("update_tags")
        with transaction.atomic():
            article = Article.objects.create(
                **validated_data, company_id=company_id, is_visible=True
            )
            tags = []
            for title in tag_titles:
                tag, created = Tag.objects.get_or_create(title=title)
                tags.append(tag)
            article.tags.set(tags)
        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления статьи"""

    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    tags = serializers.SlugRelatedField(many=True, slug_field="title", read_only=True)
    update_tags = serializers.ListField(
        child=serializers.CharField(max_length=30), write_only=True
    )
    view_count = serializers.IntegerField(read_only=True)
    is_visible = serializers.BooleanField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def update(self, instance, validated_data):
        from image.tasks import cleaner

        # delete not using image with celery worker

        if instance.image:
            object_image_id = instance.image.id
            new_image_id = validated_data.get("image")
            if new_image_id:
                new_image_id = new_image_id.id

            cleaner.delay(object_image_id, new_image_id)

        # tags block
        tag_titles = validated_data.pop("update_tags")
        tags = []
        for title in tag_titles:
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class ArticleUpdateVisionSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости статьи"""

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = [
            "company_id",
            "image",
            "name",
            "description",
            "is_visible",
            "tags",
            "view_count",
        ]

    def update(self, instance: Article, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True

        instance.save()
        return instance
