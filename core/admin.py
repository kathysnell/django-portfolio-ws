from django.contrib import admin
from django.utils.html import format_html
from .models import WebpOrLegacyBackgroundImage

class BaseImageAdminMixin:
    # Mixin to provide webp and legacy image support in inherited classes
    # Fields to show in the main list table
    list_display = ('id', 'image_name')
    
    # Fields to show in the edit form
    fields = ('image',)
    readonly_fields = ('image_name',) 

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; height: auto;" />', obj.image.url)
        return "No Image"

    def image_name(self, obj):
        return obj.image.name if obj.image else "None"

@admin.register(WebpOrLegacyBackgroundImage)
class WebpOrLegacyBackgroundAdmin(BaseImageAdminMixin, admin.ModelAdmin):
    def get_model_perms(self, request):
        # Prevent mixin from showing in main admin view
        return {}
