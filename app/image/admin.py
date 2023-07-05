from django.contrib import admin
from django.utils.safestring import mark_safe
from image.models import Image, File


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj: Image):
        return mark_safe(
            '<img src="%s" style="width: 45px; height:45px;" />' % obj.image.url
        )

    image_tag.short_description = "Image"
    list_display = ("id", "image", "image_tag")


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def file_tag(self, obj: File):
        return mark_safe(
            '<img src="%s" style="width: 45px; height:45px;" />' % obj.pdf.url
        )

    file_tag.short_description = "Pdf"
    list_display = ("id", "pdf", "file_tag")
