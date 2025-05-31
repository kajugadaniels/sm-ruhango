from base.models import Amenity
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Populate the Amenity table with a predefined list of amenities."

    AMENITIES = [
        "Towels",
        "Bath or shower",
        "Private bathroom",
        "Toilet",
        "Free toiletries",
        "Hairdryer",
        "Bath",
        "Flat-screen TV",
        "Satellite channels",
        "Radio",
        "Telephone",
        "TV",
        "Fire extinguishers",
        "CCTV in common areas",
        "Smoke alarms",
        "24-hour security",
        "Linen",
        "Wardrobe or closet",
        "Kid meals",
        "Special diet menus (on request)",
        "Breakfast in the room",
        "Bar",
        "Restaurant",
        "Tea/Coffee maker",
        "Hypoallergenic",
        "Non-smoking throughout",
        "Wake-up service",
        "Heating",
        "Packed lunches",
        "Carpeted",
        "Lift",
        "Fan",
        "Family rooms",
        "Facilities for disabled guests",
        "Ironing facilities",
        "Non-smoking rooms",
        "Iron",
        "Room service",
        "Invoice provided",
        "Private check-in/check-out",
        "Luggage storage",
        "24-hour front desk",
        "Daily housekeeping",
        "Dry cleaning",
        "Laundry",
    ]

    def handle(self, *args, **options):
        created = 0
        for name in self.AMENITIES:
            amenity, was_created = Amenity.objects.get_or_create(name=name)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f"✅ {created} amenities created (or already existed)."
        ))
