from django.db import models

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