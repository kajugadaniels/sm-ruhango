import os
from django.db import models
from django.utils.text import slugify
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField

class MassSchedule(models.Model):
    MORNING = 'morning'
    EVENING = 'evening'
    MASS_TYPE_CHOICES = [
        (MORNING, 'Morning Mass'),
        (EVENING, 'Evening Mass'),
    ]

    date = models.DateField(help_text="Date of the mass (YYYY-MM-DD)")
    start_time = models.TimeField(help_text="Start time (HH:MM)")
    end_time = models.TimeField(help_text="End time (HH:MM)")
    mass_type = models.CharField(
        max_length=10,
        choices=MASS_TYPE_CHOICES,
        default=MORNING,
        help_text="Morning or Evening"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = "Mass Schedule"
        verbose_name_plural = "Mass Schedules"

    def __str__(self):
        # e.g. "Morning Mass on 2025-05-28 at 08:00"
        return f"{self.get_mass_type_display()} on {self.date.isoformat()} at {self.start_time.strftime('%H:%M')}"

def homily_image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    return f'homilies/homily_{slugify(instance.title_en)}_{file_extension}'

class Homily(models.Model):
    """
    A multilingual homily entry, with image support (auto-resized/cropped)
    and rich-text descriptions via CKEditor for each language.
    """

    published_at = models.DateField(
        help_text="Date of the homily (YYYY-MM-DD)",
        blank=True,
        null=True,
    )

    # Multilingual titles
    title_en = models.CharField(max_length=200, help_text="Title in English")
    title_fr = models.CharField(max_length=200, help_text="Titre en Français")
    title_rw = models.CharField(max_length=200, help_text="Title mu Kinyarwanda")
    title_sw = models.CharField(max_length=200, help_text="Title kwa Kiswahili")

    # Multilingual rich-text content fields
    content_en = RichTextUploadingField(blank=True, help_text="Content in English")
    content_fr = RichTextUploadingField(blank=True, help_text="Contenu en Français")
    content_rw = RichTextUploadingField(blank=True, help_text="Content mu Kinyarwanda")
    content_sw = RichTextUploadingField(blank=True, help_text="Content kwa Kiswahili")
    image = ProcessedImageField(
        upload_to=homily_image_path,
        processors=[ResizeToFill(1270, 1270)],
        format='JPEG',
        options={'quality': 90},
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Homily"
        verbose_name_plural = "Homilies"

    def __str__(self):
        # Display with English title and date for quick reference
        date_str = self.published_at.isoformat() if self.published_at else "No date"
        return f"{self.title_en} ({date_str})"

def event_image_path(instance, filename):
    """
    Generate a unique file path for event images:
    events/event_<slug>_<date><extension>
    """
    base_filename, file_extension = os.path.splitext(filename)
    slug = slugify(instance.title_en)
    date_str = instance.event_date.isoformat()
    return f"events/event_{slug}_{date_str}{file_extension}"


class Event(models.Model):
    """
    A professional, multilingual Event model for SM Ruhango:
    - Supports English, Français, Kinyarwanda, Kiswahili
    - Automatic slug generation
    - Rich text descriptions via CKEditor
    - Image handling with automatic resize & crop
    """

    # Scheduling fields
    event_date = models.DateField(help_text="Event date (YYYY-MM-DD)")
    start_time = models.TimeField(help_text="Start time (HH:MM)", blank=True, null=True)
    end_time = models.TimeField(help_text="End time (HH:MM)", blank=True, null=True)

    # URL slug
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Auto-generated from English title and date."
    )

    # Multilingual titles
    title_en = models.CharField(max_length=200, help_text="Title in English")
    title_fr = models.CharField(max_length=200, help_text="Titre en Français")
    title_rw = models.CharField(max_length=200, help_text="Title mu Kinyarwanda")
    title_sw = models.CharField(max_length=200, help_text="Title kwa Kiswahili")

    # Multilingual rich-text descriptions
    description_en = RichTextUploadingField(blank=True, help_text="Description in English")
    description_fr = RichTextUploadingField(blank=True, help_text="Description en Français")
    description_rw = RichTextUploadingField(blank=True, help_text="Description mu Kinyarwanda")
    description_sw = RichTextUploadingField(blank=True, help_text="Description kwa Kiswahili")

    # Image with automatic resizing & cropping
    image = ProcessedImageField(
        upload_to=event_image_path,
        processors=[ResizeToFill(1200, 800)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True,
        help_text="Main banner image for the event; auto-cropped and resized."
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date', 'start_time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):
        """
        Auto-generate slug on first save.
        """
        if not self.slug:
            base_slug = slugify(self.title_en)
            date_str = self.event_date.isoformat()
            self.slug = f"{base_slug}-{date_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title_en} on {self.event_date.isoformat()}"

def testimony_upload_path(instance, filename):
    """
    Files (audio/video) get saved under MEDIA_ROOT/testimonies/<type>/<name>_<timestamp><ext>
    """
    base, ext = os.path.splitext(filename)
    safe_name = instance.name.replace(" ", "_")
    return f"testimonies/{instance.testimony_type}/{safe_name}_{instance.id}{ext}"


class Testimony(models.Model):
    """
    A model to capture user testimonies in text, audio, or video format.
    Admin chooses whether a testimony is published or kept as draft.
    """
    # Type of testimony
    TEXT  = "text"
    AUDIO = "audio"
    VIDEO = "video"
    TYPE_CHOICES = [
        (TEXT,  "Text"),
        (AUDIO, "Audio"),
        (VIDEO, "Video"),
    ]

    # Status (admin-only field)
    DRAFT     = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (DRAFT,     "Draft"),
        (PUBLISHED, "Published"),
    ]

    # Who is giving the testimony
    name  = models.CharField(
        max_length=150,
        help_text="Full name of the person giving the testimony",
    )
    email = models.EmailField(
        help_text="Contact email of the testimony giver"
    )

    # What format: text vs audio vs video
    testimony_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=TEXT,
        help_text="Select whether this is a text, audio, or video testimony",
    )

    # Content fields: only one will be used depending on testimony_type
    content_text = models.TextField(
        blank=True,
        help_text="Enter the full text of the testimony (if type is Text)."
    )

    content_file = models.FileField(
        upload_to=testimony_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['mp3', 'wav', 'mp4', 'mov']
        )],
        blank=True,
        help_text=(
            "Upload an audio (mp3/wav) or video (mp4/mov) file. "
            "Required if type is Audio or Video."
        )
    )

    # Admin-only published status
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text="Set to Published when the testimony is approved to go live."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimony"
        verbose_name_plural = "Testimonies"

    def __str__(self):
        return f"{self.name} ({self.get_testimony_type_display()}) - {self.status.capitalize()}"

def advertisement_image_path(instance, filename):
    """
    Store images under MEDIA_ROOT/advertisements/<slug>_<date><ext>
    """
    base, ext = os.path.splitext(filename)
    slug = slugify(instance.title_en)
    date_str = instance.published_at.isoformat()
    return f"advertisements/{slug}_{date_str}{ext}"


class Advertisement(models.Model):
    """
    A professional, multilingual Advertisement model:
    - Four-language titles & content
    - Banner image with resizing/cropping
    - Publication date field
    """

    # When this advert is published
    published_at = models.DateField(
        help_text="Publication date (YYYY-MM-DD)",
        blank=True,
        null=True,
    )

    # Multilingual titles
    title_en = models.CharField(max_length=200, help_text="Title in English")
    title_fr = models.CharField(max_length=200, help_text="Titre en Français")
    title_rw = models.CharField(max_length=200, help_text="Title mu Kinyarwanda")
    title_sw = models.CharField(max_length=200, help_text="Title kwa Kiswahili")

    # Multilingual rich-text content fields
    content_en = RichTextUploadingField(blank=True, help_text="Content in English")
    content_fr = RichTextUploadingField(blank=True, help_text="Contenu en Français")
    content_rw = RichTextUploadingField(blank=True, help_text="Content mu Kinyarwanda")
    content_sw = RichTextUploadingField(blank=True, help_text="Content kwa Kiswahili")

    # Banner image with automatic resize & crop
    image = ProcessedImageField(
        upload_to=advertisement_image_path,
        processors=[ResizeToFill(1200, 600)],
        format='JPEG',
        options={'quality': 85},
        blank=True,
        null=True,
        help_text="Main banner image; auto-resized/cropped to 1200×600.",
    )

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        date_str = self.published_at.isoformat() if self.published_at else "No date"
        return f"{self.title_en} ({date_str})"