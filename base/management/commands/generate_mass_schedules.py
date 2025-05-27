from django.core.management.base import BaseCommand
from datetime import date, time, timedelta
from base.models import MassSchedule

class Command(BaseCommand):
    help = (
        "Generate daily morning and evening MassSchedule entries "
        "from January 1, 2025 through June 30, 2025."
    )

    def handle(self, *args, **options):
        start_date = date(2025, 1, 1)
        end_date   = date(2025, 6, 30)
        one_day    = timedelta(days=1)
        current    = start_date
        created    = 0

        while current <= end_date:
            # Morning Mass
            ms_morning = MassSchedule(
                date=current,
                start_time=time(8,  0),
                end_time=  time(9,  0),
                mass_type=MassSchedule.MORNING,
            )
            ms_morning.save()
            created += 1

            # Evening Mass
            ms_evening = MassSchedule(
                date=current,
                start_time=time(18, 0),
                end_time=  time(19, 0),
                mass_type=MassSchedule.EVENING,
            )
            ms_evening.save()
            created += 1

            current += one_day

        self.stdout.write(self.style.SUCCESS(
            f"✅ Generated {created} MassSchedule entries "
            f"({(created//2)} days × 2 masses)"
        ))
