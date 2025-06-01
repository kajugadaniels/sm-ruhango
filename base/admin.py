from base.models import *
from django.contrib import admin
from django.utils.html import format_html

@admin.register(MassSchedule)
class MassScheduleAdmin(admin.ModelAdmin):
    # Columns shown in the changelist
    list_display   = ('date', 'start_time', 'end_time', 'mass_type')
    list_filter    = ('mass_type', 'date')
    ordering       = ('-date', 'start_time')
    list_per_page  = 20

    # Group and label fields for clarity; collapse verbose descriptions by default
    fieldsets = (
        ('Schedule Details', {
            'fields': ('date', ('start_time', 'end_time'), 'mass_type'),
            'description': 'Pick the date, times and whether it’s a morning or evening Mass.'
        }),
    )

@admin.register(Homily)
class HomilyAdmin(admin.ModelAdmin):
    # Columns in the changelist view
    list_display   = ('published_at', 'title_en', 'image_preview')
    list_filter    = ('published_at',)
    search_fields  = (
        'title_en','title_fr','title_rw','title_sw',
        'content_en','content_fr','content_rw','content_sw'
    )
    ordering       = ('-published_at',)
    list_per_page  = 20

    # Make the preview read-only
    readonly_fields = ('image_preview',)

    # Logical grouping of fields
    fieldsets = (
        ('Publication', {
            'fields': ('published_at',),
            'description': 'Optional date for archiving or sorting your homilies.'
        }),
        ('Titles (required)', {
            'fields': ('title_en', 'title_fr', 'title_rw', 'title_sw'),
            'description': 'Enter the homily title in each language.'
        }),
        ('Content (rich text)', {
            'classes': ('collapse',),
            'fields': ('content_en', 'content_fr', 'content_rw', 'content_sw'),
            'description': 'Use the CKEditor to craft your homily content per language. Collapsed by default for a cleaner UI.'
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload a main image (auto-resized/cropped). A preview is shown below.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" style="object-fit: cover; border-radius:4px;" />',
                obj.image.url
            )
        return "(No image)"
    image_preview.short_description = 'Preview'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin interface for Event:
    - Searchable multilingual fields
    - Collapsible rich text descriptions
    - Image preview
    - Slug is read-only
    """
    list_display   = ('event_date', 'title_en', 'slug', 'image_preview')
    list_filter    = ('event_date',)
    search_fields  = (
        'title_en','title_fr','title_rw','title_sw',
        'description_en','description_fr','description_rw','description_sw'
    )
    ordering       = ('-event_date',)
    list_per_page  = 20
    readonly_fields = ('slug', 'image_preview')

    fieldsets = (
        ('Schedule', {
            'fields': ('event_date', ('start_time', 'end_time')),
            'description': 'When this event takes place.'
        }),
        ('Titles & Slug', {
            'fields': (
                'title_en','title_fr','title_rw','title_sw', 'slug'
            ),
            'description': 'Enter the title in each language; slug auto-generated.'
        }),
        ('Descriptions (rich text)', {
            'classes': ('collapse',),
            'fields': (
                'description_en','description_fr',
                'description_rw','description_sw'
            ),
            'description': 'Detailed event description per language.'
        }),
        ('Media', {
            'fields': ('image','image_preview'),
            'description': 'Upload a banner image; preview shown below.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="30" style="object-fit: cover; border-radius:4px;" />',
                obj.image.url
            )
        return "(No image)"
    image_preview.short_description = 'Banner Preview'

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    """
    Admin interface for Testimony:
    - Display name, email, type, status, and creation date
    - Filter by type & status
    - Inline preview/link for uploaded file
    """
    list_display   = ('name', 'email', 'testimony_type', 'status', 'created_at', 'file_link')
    list_filter    = ('testimony_type', 'status', 'created_at')
    search_fields  = ('name', 'email', 'content_text')
    ordering       = ('-created_at',)
    list_per_page  = 20

    readonly_fields = ('file_link',)

    fieldsets = (
        ("Testimony Info", {
            'fields': (
                'name', 'email', 'testimony_type', 'status'
            ),
            'description': (
                "Fill in the person’s name/email and select the testimony type. "
                "Admin uses 'Status' to control publication."
            )
        }),
        ("Content (one of the following)", {
            'fields': (
                'content_text', 'content_file', 'file_link'
            ),
            'description': (
                "If the type is Text, fill in content_text. "
                "If Audio or Video, upload under content_file. "
                "File link is read-only and shows after upload."
            )
        }),
    )

    def file_link(self, obj):
        """
        Provide a clickable link for audio/video files, or indicate N/A if none.
        """
        if obj.content_file:
            url = obj.content_file.url
            filename = obj.content_file.name.split('/')[-1]
            return format_html('<a href="{}" target="_blank">{}</a>', url, filename)
        return "(No file)"
    file_link.short_description = "Uploaded File"

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """
    Admin interface for Advertisement:
    - Show publication date, English title, and image preview
    - Filter by published_at date
    - Search across all multilingual titles & contents
    - Collapsible sections for content
    """
    list_display   = ('published_at', 'title_en', 'image_preview')
    list_filter    = ('published_at',)
    search_fields  = (
        'title_en','title_fr','title_rw','title_sw',
        'content_en','content_fr','content_rw','content_sw'
    )
    ordering       = ('-published_at', '-created_at')
    list_per_page  = 20

    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Publication', {
            'fields': ('published_at',),
            'description': 'Set the date this advertisement goes live.'
        }),
        ('Titles (required)', {
            'fields': ('title_en', 'title_fr', 'title_rw', 'title_sw'),
            'description': 'Enter the advertisement title in each language.'
        }),
        ('Content (rich text)', {
            'classes': ('collapse',),
            'fields': ('content_en', 'content_fr', 'content_rw', 'content_sw'),
            'description': 'Use CKEditor to craft the full ad copy in each language. Collapsed by default.'
        }),
        ('Banner Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Upload the banner image; preview appears below.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="30" style="object-fit: cover; border-radius:4px;" />',
                obj.image.url
            )
        return "(No image)"
    image_preview.short_description = "Image Preview"

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """
    Manage Amenity entries.
    """
    list_display  = ('name',)
    search_fields = ('name',)
    ordering      = ('name',)
    list_per_page = 20

class RoomImageInline(admin.TabularInline):
    """
    Inline for RoomImage to upload/display multiple images per room.
    """
    model = RoomImage
    extra = 1
    readonly_fields = ('image_tag',)
    fields = ('image', 'alt_text', 'image_tag')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Admin interface for Room:
    - Manage title, slug, location, description, price, & amenities
    - Inline RoomImage uploads
    - Show thumbnail previews of room images
    """
    list_display   = ('title', 'location', 'price_per_night', 'thumbnail_preview')
    list_filter    = ('location', 'amenities')
    search_fields  = ('title', 'location', 'description')
    ordering       = ('title',)
    list_per_page  = 20

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'location', 'price_per_night'),
            'description': 'Basic room details. Slug will be auto-generated.'
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',),
            'description': 'Rich-text description of the room.'
        }),
        ('Amenities', {
            'fields': ('amenities',),
            'description': 'Select multiple amenities available in this room.'
        }),
    )
    readonly_fields = ('slug',)
    inlines = [RoomImageInline]

    def thumbnail_preview(self, obj):
        """
        Show the first image as a small preview.
        """
        first_image = obj.images.first()
        if first_image:
            return format_html(
                '<img src="{}" width="100" style="object-fit: cover; border-radius:4px;"/>',
                first_image.image.url
            )
        return "(No image)"

    thumbnail_preview.short_description = 'Thumbnail'

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
    Admin interface for Gallery:
    - Show created_at, English caption, and a thumbnail
    - Searchable multilingual captions
    - Image preview
    """
    list_display    = ("created_at", "caption_en", "image_preview")
    search_fields   = ("caption_en", "caption_fr", "caption_rw", "caption_sw")
    ordering        = ("-created_at",)
    list_filter     = ("created_at",)
    readonly_fields = ("image_preview",)

    fieldsets = (
        (
            "Captions",
            {
                "fields": ("caption_en", "caption_fr", "caption_rw", "caption_sw"),
                "description": "Enter optional captions in English, French, Kinyarwanda, and Kiswahili.",
            },
        ),
        (
            "Image",
            {
                "fields": ("image", "image_preview"),
                "description": "Upload the image for the gallery item; preview shown below.",
            },
        ),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" style="object-fit: cover; border-radius:4px;" />',
                obj.image.url,
            )
        return "(No image)"

    image_preview.short_description = "Thumbnail"

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Admin interface for Member:
    - Show name, role, and thumbnail
    - Filter by role
    - Search by name
    """
    list_display    = ('name', 'get_role_display', 'thumbnail')
    list_filter     = ('role',)
    search_fields   = ('name',)
    ordering        = ('name',)
    readonly_fields = ('thumbnail',)

    fieldsets = (
        (None, {
            'fields': ('name', 'role'),
            'description': 'Enter the member’s full name and select their role (Priest or Board Member).'
        }),
        ('Portrait Image', {
            'fields': ('image', 'thumbnail'),
            'description': 'Upload a square portrait (will be resized to 400×400). Thumbnail shown below.'
        }),
    )

    def thumbnail(self, obj):
        """
        Display a small thumbnail of the member’s portrait.
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="75" height="75" style="object-fit: cover; border-radius:50%;" />',
                obj.image.url
            )
        return "(No image)"

    thumbnail.short_description = "Portrait"

@admin.register(HealingPrayer)
class HealingPrayerAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('title_en', 'title_fr', 'title_rw', 'title_sw', 'content_en', 'content_fr', 'content_rw', 'content_sw')
    ordering = ('-created_at',)
    list_per_page = 20

    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Healing Prayer Details', {
            'fields': ('title_en', 'title_fr', 'title_rw', 'title_sw', 'content_en', 'content_fr', 'content_rw', 'content_sw', 'image', 'image_preview'),
            'description': 'Enter the healing prayer details in all four languages. The image will be displayed alongside the prayer text.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" style="object-fit: cover; border-radius:4px;" />',
                obj.image.url
            )
        return "(No image)"
    image_preview.short_description = 'Image Preview'