import os
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from django.utils.text import slugify
from base.models import Member

class Command(BaseCommand):
    help = "Generate 20 fake church Members with Rwanda names and square portraits"

    def handle(self, *args, **options):
        # Use Kinyarwanda locale if available; otherwise default to en
        try:
            fake = Faker("rw_RW")
        except Exception:
            fake = Faker()

        output_dir = os.path.join(settings.MEDIA_ROOT, "members")
        os.makedirs(output_dir, exist_ok=True)

        ROLES = ["priest", "board"]

        def create_square_mosaic(size):
            """
            Create a simple 400×400 mosaic by dividing into 4 quadrants,
            each with a random color.
            """
            img = Image.new("RGB", (size, size))
            draw = ImageDraw.Draw(img)
            half = size // 2
            quads = [
                (0, 0, half, half),
                (half, 0, size, half),
                (0, half, half, size),
                (half, half, size, size),
            ]
            for quad in quads:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.rectangle(quad, fill=color)
            return img

        created_count = 0

        for i in range(1, 21):
            # Generate a Rwandan-style name
            name = fake.name()
            role = random.choice(ROLES)

            member = Member(name=name, role=role)
            member.save()  # need to save to get ID for slug/path

            # Create and save a 400×400 mosaic portrait
            size = 400
            img = create_square_mosaic(size)
            slug = slugify(name)
            filename = f"{slug}_{member.id}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)

            # Assign image field and save again
            member.image = f"members/{filename}"
            member.save()

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {created_count} Member entries.")
        )
