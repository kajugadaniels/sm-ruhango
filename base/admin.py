from base.models import *
from django.contrib import admin

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
