from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Article, Commenter, Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title_ar", "published_at", "is_published")
    list_filter = ("is_published", "published_at")
    prepopulated_fields = {"slug": ("title_en",)}
    search_fields = ("title_ar", "title_en")

@admin.register(Commenter)
class CommenterAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("name", "email")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "article", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("commenter__name", "content")
