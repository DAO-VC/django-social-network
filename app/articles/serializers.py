from rest_framework import serializers

from articles.models import Article
from profiles.models import Startup


class ArticleCreateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        company_id = Startup.objects.filter(owner=self.context["request"].user).first()
        article = Article.objects.create(**validated_data, company_id=company_id)
        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    company_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Article
        fields = "__all__"
