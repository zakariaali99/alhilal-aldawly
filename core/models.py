from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteSettings(models.Model):
    logo = models.ImageField(_("Logo"), upload_to="settings/")
    favicon = models.ImageField(_("Favicon"), upload_to="settings/", blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=20)
    phone_whatsapp = models.CharField(_("WhatsApp Phone"), max_length=20, blank=True)
    email = models.EmailField(_("Email"))
    address_ar = models.TextField(_("Address (Ar)"))
    address_en = models.TextField(_("Address (En)"))
    google_maps_embed = models.TextField(_("Google Maps Embed Code"), blank=True, help_text=_("Paste your Google Maps iframe code here"))
    facebook = models.URLField(_("Facebook"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return str(_("Site Settings"))

class HeroSection(models.Model):
    title_ar = models.CharField(_("Title (Ar)"), max_length=200)
    title_en = models.CharField(_("Title (En)"), max_length=200)
    subtitle_ar = models.TextField(_("Subtitle (Ar)"))
    subtitle_en = models.TextField(_("Subtitle (En)"))
    image = models.ImageField(_("Background Image"), upload_to="hero/")
    cta_text_ar = models.CharField(_("CTA Text (Ar)"), max_length=50)
    cta_text_en = models.CharField(_("CTA Text (En)"), max_length=50)
    cta_link = models.CharField(_("CTA Link"), max_length=200, default="#")
    is_active = models.BooleanField(_("Is Active"), default=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Hero Section")
        verbose_name_plural = _("Hero Sections")
        ordering = ["order"]

    def __str__(self):
        return self.title_ar

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    is_read = models.BooleanField(_("Is Read"), default=False)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
