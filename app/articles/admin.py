from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from articles.models import Article, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["image"].disabled = True
        return form

    list_display = ("id", "name", "company_link", "is_visible", "created_at")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    list_filter = ("is_visible", ("company_id", admin.RelatedOnlyFieldListFilter))
    ordering = (
        "id",
        "created_at",
        "is_visible",
    )
    filter_horizontal = ("tags",)

    def company_link(self, article: Article):
        url = reverse("admin:profiles_startup_change", args=[article.company_id.id])
        link = '<a href="%s">%s</a>' % (url, article.company_id.id)
        return mark_safe(link)

    company_link.short_description = "Владелец"
