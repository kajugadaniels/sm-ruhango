from base.models import *
from django.contrib import admin

@admin.register(MassSchedule)
class MassScheduleAdmin(admin.ModelAdmin):
    # Columns shown in the changelist
    list_display   = ('date', 'start_time', 'end_time', 'mass_type', 'title_en')
    list_filter    = ('mass_type', 'date')
    search_fields  = (
        'title_en','title_fr','title_rw','title_sw',
        'description_en','description_fr','description_rw','description_sw'
    )
    ordering       = ('-date', 'start_time')
    list_per_page  = 20

    # Group and label fields for clarity; collapse verbose descriptions by default
    fieldsets = (
        ('Schedule Details', {
            'fields': ('date', ('start_time', 'end_time'), 'mass_type'),
            'description': 'Pick the date, times and whether it’s a morning or evening Mass.'
        }),
        ('Titles (Required)', {
            'fields': ('title_en', 'title_fr', 'title_rw', 'title_sw'),
            'description': 'Enter the title exactly as you want it to appear in each language.'
        }),
        ('Descriptions (Optional)', {
            'classes': ('collapse',),
            'fields': (
                'description_en','description_fr',
                'description_rw','description_sw'
            ),
            'description': 'Add extra context or notes in each language. Can be left blank.'
        }),
    )
