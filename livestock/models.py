from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os
from django.conf import settings
from django.core.files import File

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
    mute_video = models.BooleanField(_("Mute Video"), default=True, help_text=_("Mute video audio permanently to reduce size and auto-play quietly."))
    caption_ar = models.CharField(_("Caption (Ar)"), max_length=200, blank=True)
    caption_en = models.CharField(_("Caption (En)"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Category Media")
        verbose_name_plural = _("Category Media Items")
        ordering = ["order"]

    def __str__(self):
        return f"{self.category.name_ar} - {self.media_type}"

    def save(self, *args, **kwargs):
        # Check if file is new or changed and is a video
        if self.pk:
            old_instance = CategoryMedia.objects.get(pk=self.pk)
            if old_instance.file != self.file:
                self.process_video()
        elif self.file: # New instance with file
             self.process_video()
        
        super().save(*args, **kwargs)

    def process_video(self):
        if self.media_type == 'video' and self.file:
            try:
                import subprocess
                import tempfile
                
                # Write uploaded file to a temp input file
                suffix = os.path.splitext(self.file.name)[-1] or '.mov'
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_in:
                    for chunk in self.file.chunks():
                        tmp_in.write(chunk)
                    input_path = tmp_in.name
                
                # Build output path
                output_path = input_path + '_out.mp4'
                
                # Build ffmpeg command
                cmd = [
                    'ffmpeg', '-y', '-i', input_path,
                    '-map', '0:v:0',          # only first video stream
                ]
                
                # Audio: either mute or keep first audio stream
                if self.mute_video:
                    cmd += ['-an']  # no audio
                else:
                    cmd += ['-map', '0:a:0?', '-c:a', 'aac', '-b:a', '128k']
                
                # Video encoding: H.264, scale to max 720 wide, cap fps at 24
                cmd += [
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '28',
                    '-vf', 'scale=720:-2:force_original_aspect_ratio=decrease',
                    '-r', '24',
                    '-movflags', '+faststart',
                    output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    # Replace the uploaded file with the processed one
                    base_name = os.path.splitext(os.path.basename(self.file.name))[0] + '.mp4'
                    with open(output_path, 'rb') as f:
                        self.file.save(base_name, File(f), save=False)
                else:
                    print(f"FFmpeg error: {result.stderr[-500:] if result.stderr else 'unknown'}")
                
                # Cleanup
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
                    
            except Exception as e:
                print(f"Error processing video: {e}")

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
    mute_video = models.BooleanField(_("Mute Video"), default=True, help_text=_("Mute video audio permanently to reduce size and auto-play quietly."))
    caption_ar = models.CharField(_("Caption (Ar)"), max_length=200, blank=True)
    caption_en = models.CharField(_("Caption (En)"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)

    class Meta:
        verbose_name = _("Gallery Item")
        verbose_name_plural = _("Gallery Items")
        ordering = ["order"]

    def __str__(self):
        return f"{self.livestock_item.title_ar} - {self.media_type}"

    def save(self, *args, **kwargs):
        # Check if file is new or changed and is a video
        if self.pk:
            old_instance = MediaGalleryItem.objects.get(pk=self.pk)
            if old_instance.file != self.file:
                self.process_video()
        elif self.file: # New instance with file
             self.process_video()
        
        super().save(*args, **kwargs)

    def process_video(self):
        if self.media_type == 'video' and self.file:
            try:
                import subprocess
                import tempfile
                
                # Write uploaded file to a temp input file
                suffix = os.path.splitext(self.file.name)[-1] or '.mov'
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp_in:
                    for chunk in self.file.chunks():
                        tmp_in.write(chunk)
                    input_path = tmp_in.name
                
                # Build output path
                output_path = input_path + '_out.mp4'
                
                # Build ffmpeg command
                cmd = [
                    'ffmpeg', '-y', '-i', input_path,
                    '-map', '0:v:0',          # only first video stream
                ]
                
                # Audio: either mute or keep first audio stream
                if self.mute_video:
                    cmd += ['-an']  # no audio
                else:
                    cmd += ['-map', '0:a:0?', '-c:a', 'aac', '-b:a', '128k']
                
                # Video encoding: H.264, scale to max 720 wide, cap fps at 24
                cmd += [
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '28',
                    '-vf', 'scale=720:-2:force_original_aspect_ratio=decrease',
                    '-r', '24',
                    '-movflags', '+faststart',
                    output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    # Replace the uploaded file with the processed one
                    base_name = os.path.splitext(os.path.basename(self.file.name))[0] + '.mp4'
                    with open(output_path, 'rb') as f:
                        self.file.save(base_name, File(f), save=False)
                else:
                    print(f"FFmpeg error: {result.stderr[-500:] if result.stderr else 'unknown'}")
                
                # Cleanup
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
                    
            except Exception as e:
                print(f"Error processing video: {e}")
