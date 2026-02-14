from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Category(models.Model):
    name_ar = models.CharField(_("Name (Ar)"), max_length=100)
    name_en = models.CharField(_("Name (En)"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_("Parent Category"))
    description_ar = models.TextField(_("Description (Ar)"), blank=True)
    description_en = models.TextField(_("Description (En)"), blank=True)
    icon = models.ImageField(_("Icon"), upload_to="categories/", blank=True, null=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["order"]

    def __str__(self):
        return self.name_ar

class CategoryMedia(models.Model):
    MEDIA_TYPES = (
        ("image", _("Image")),
        ("video", _("Video")),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="media", verbose_name=_("Category"))
    media_type = models.CharField(_("Media Type"), max_length=10, choices=MEDIA_TYPES, default="image")
    file = models.FileField(_("File"), upload_to="category_media/")
    caption_ar = models.CharField(_("Caption (Ar)"), max_length=200, blank=True)
    caption_en = models.CharField(_("Caption (En)"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Category Media")
        verbose_name_plural = _("Category Media Items")
        ordering = ["order"]

    def __str__(self):
        return f"{self.category.name_ar} - {self.media_type}"

class LivestockItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items", verbose_name=_("Category"))
    title_ar = models.CharField(_("Title (Ar)"), max_length=200)
    title_en = models.CharField(_("Title (En)"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    description_ar = models.TextField(_("Description (Ar)"))
    description_en = models.TextField(_("Description (En)"))
    featured_image = models.ImageField(_("Featured Image"), upload_to="livestock/")
    is_featured = models.BooleanField(_("Is Featured"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Livestock Item")
        verbose_name_plural = _("Livestock Items")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_ar

class MediaGalleryItem(models.Model):
    MEDIA_TYPES = (
        ("image", _("Image")),
        ("video", _("Video")),
    )
    livestock_item = models.ForeignKey(LivestockItem, on_delete=models.CASCADE, related_name="gallery", verbose_name=_("Livestock Item"))
    media_type = models.CharField(_("Media Type"), max_length=10, choices=MEDIA_TYPES, default="image")
    file = models.FileField(_("File"), upload_to="livestock_gallery/")
    caption_ar = models.CharField(_("Caption (Ar)"), max_length=200, blank=True)
    caption_en = models.CharField(_("Caption (En)"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Gallery Item")
        verbose_name_plural = _("Gallery Items")
        ordering = ["order"]

    def __str__(self):
        return f"{self.livestock_item.title_ar} - {self.media_type}"
