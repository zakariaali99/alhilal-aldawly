from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SiteSettings, HeroSection, ContactMessage

admin.site.site_header = _("لوحة تحكم الهلال الدولي")
admin.site.site_title = _("الهلال الدولي")
admin.site.index_title = _("إدارة الموقع")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone")
    
    def has_add_permission(self, request):
        # Only one site settings object allowed
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title_ar", "is_active", "order")
    list_editable = ("is_active", "order")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    search_fields = ("name", "email", "subject")
