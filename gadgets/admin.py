from django.contrib import admin
from .models import Gadget

class GadgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'ram', 'storage', 'reviews_count', 'average_rating', 'image_preview')
    list_filter = ('category',)

    def image_preview(self, obj):
        return obj.image.url if obj.image else "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Gadget, GadgetAdmin)
