from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from articles.models import Article, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title_link",
    )

    def title_link(self, tag: Tag):
        url = reverse("admin:articles_tag_change", args=[tag.id])
        link = '<a href="%s">%s</a>' % (url, tag.title)
        return mark_safe(link)

    title_link.short_description = "Название"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields["image"].disabled = True
    #     return form

    list_display = ("id", "name_link", "company_link", "is_visible", "created_at")
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
    autocomplete_fields = ("image",)

    def company_link(self, article: Article):
        url = reverse("admin:profiles_startup_change", args=[article.company_id.id])
        link = '<a href="%s">%s</a>' % (
            url,
            f"{article.company_id.id}-{article.company_id.name}",
        )
        return mark_safe(link)

    company_link.short_description = "Владелец"

    def name_link(self, article: Article):
        url = reverse("admin:articles_article_change", args=[article.id])
        link = '<a href="%s">%s</a>' % (url, article.name)
        return mark_safe(link)

    name_link.short_description = "Заголовок"
