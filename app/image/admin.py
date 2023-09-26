from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from image.models import Image, File


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # def has_module_permission(self, request):
    #     return False

    def image_tag(self, obj: Image):
        return mark_safe(
            '<img src="%s" style="width: 250px; height:250px;" />' % obj.image.url
        )

    def title_link(self, image: Image):
        url = reverse("admin:image_image_change", args=[image.id])
        link = '<a href="%s">%s</a>' % (url, image.image)
        return mark_safe(link)

    title_link.short_description = "Image"

    #
    # image_tag.short_description = "Image"
    list_display = ("id", "image_tag")
    # readonly_fields = ("image_tag",)
    search_fields = ("id", "image__contains")
    readonly_fields = ("image_tag",)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

    def file_tag(self, obj: File):
        return mark_safe(
            '<img src="%s" style="width: 250px; height:250px;" />' % obj.pdf.url
        )

    file_tag.short_description = "Pdf"
    list_display = ("id", "file_tag")
    # readonly_fields = ("file_tag",)
    search_fields = ("id", "pdf__contains")
