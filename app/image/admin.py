from django.contrib import admin

from image.models import Image, File


@admin.register(Image)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "image")


@admin.register(File)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "pdf")
