from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class Article(models.Model):
    title_ar = models.CharField(_("Title (Ar)"), max_length=200)
    title_en = models.CharField(_("Title (En)"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    content_ar = RichTextField(_("Content (Ar)"))
    content_en = RichTextField(_("Content (En)"))
    featured_image = models.ImageField(_("Featured Image"), upload_to="news/")
    published_at = models.DateTimeField(_("Published At"), auto_now_add=True)
    is_published = models.BooleanField(_("Is Published"), default=True)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title_ar

class Commenter(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"), unique=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Commenter")
        verbose_name_plural = _("Commenters")

    def __str__(self):
        return f"{self.name} ({self.email})"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Article"))
    commenter = models.ForeignKey(Commenter, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Commenter"))
    content = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    is_approved = models.BooleanField(_("Is Approved"), default=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.commenter.name} on {self.article.title_ar}"
