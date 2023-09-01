from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.safestring import mark_safe

admin.site.unregister(Group)

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("id", "email_link", "is_onboarding", "profile")
    search_fields = (
        "email__startswith",
        "id",
    )
    list_filter = ("is_onboarding", "profile", "online")
    ordering = (
        "is_onboarding",
        "profile",
        "online",
    )
    filter_horizontal = ("users_banned_list",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "phone",
                    "is_staff",
                    "is_active",
                    "is_onboarding",
                    "profile",
                    "permissions",
                    "online",
                    "date_joined",
                    "last_login",
                    "users_banned_list",
                )
            },
        ),
        ("Change password", {"classes": ("collapse",), "fields": ("password",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "profile", "password1", "password2"),
            },
        ),
    )

    def email_link(self, user: User):
        url = reverse("admin:core_user_change", args=[user.id])
        link = '<a href="%s">%s</a>' % (url, user.email)
        return mark_safe(link)

    email_link.short_description = "Адрес электронной почты"
