from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, CategoryMedia, LivestockItem, MediaGalleryItem

class CategoryMediaInline(admin.TabularInline):
    model = CategoryMedia
    extra = 1
    fields = ('media_type', 'file', 'mute_video', 'caption_ar', 'caption_en', 'order')

class MediaGalleryInline(admin.TabularInline):
    model = MediaGalleryItem
    extra = 1
    fields = ('media_type', 'file', 'mute_video', 'caption_ar', 'caption_en', 'order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "order")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [CategoryMediaInline]

@admin.register(LivestockItem)
class LivestockItemAdmin(admin.ModelAdmin):
    list_display = ("title_ar", "category", "is_featured", "created_at")
    list_filter = ("category", "is_featured")
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [MediaGalleryInline]
    search_fields = ("title_ar", "title_en", "description_ar", "description_en")
