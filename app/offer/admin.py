from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from offer.models.offer import Offer, ConfirmedOffer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "investor_link", "is_visible", "created_at")
    search_fields = (
        "name__startswith",
        "id",
        "email__startswith",
    )
    list_filter = ("is_visible", ("investor_id", admin.RelatedOnlyFieldListFilter))
    ordering = (
        "id",
        "created_at",
        "is_visible",
    )
    filter_horizontal = ("industries",)

    def investor_link(self, offer: Offer):
        url = reverse("admin:profiles_investor_change", args=[offer.investor_id.id])
        link = '<a href="%s">%s</a>' % (url, offer.investor_id.id)
        return mark_safe(link)

    investor_link.short_description = "Инвестор"


@admin.register(ConfirmedOffer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "investor_link",
        "startup_link",
    )
    list_filter = (
        ("investor_id", admin.RelatedOnlyFieldListFilter),
        ("startup_id", admin.RelatedOnlyFieldListFilter),
    )
    ordering = ("id",)

    def startup_link(self, offer: ConfirmedOffer):
        url = reverse("admin:profiles_startup_change", args=[offer.startup_id.id])
        link = '<a href="%s">%s</a>' % (url, offer.startup_id.id)
        return mark_safe(link)

    startup_link.short_description = "Стартап"

    def investor_link(self, offer: ConfirmedOffer):
        url = reverse("admin:profiles_investor_change", args=[offer.investor_id.id])
        link = '<a href="%s">%s</a>' % (url, offer.investor_id.id)
        return mark_safe(link)

    investor_link.short_description = "Инвестор"
