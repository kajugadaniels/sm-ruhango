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