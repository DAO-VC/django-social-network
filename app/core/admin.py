from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

admin.site.unregister(Group)

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_onboarding", "profile")
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
                )
            },
        ),
        ("Change password", {"classes": ("collapse",), "fields": ("password",)}),
    )
