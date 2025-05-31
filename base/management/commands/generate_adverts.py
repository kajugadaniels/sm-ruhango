import os
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from django.utils.text import slugify
from base.models import Advertisement

class Command(BaseCommand):
    help = "Generate 20 fake Advertisement entries (April 1 2025 – July 28 2025) with images"

    def handle(self, *args, **options):
        fake = Faker()
        output_dir = os.path.join(settings.MEDIA_ROOT, "advertisements")
        os.makedirs(output_dir, exist_ok=True)

        def create_random_color():
            return tuple(random.randint(0, 255) for _ in range(3))

        def create_banner_image(width, height):
            """
            Create a 4-quadrant mosaic of random colors to serve as a banner.
            """
            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)
            w2, h2 = width // 2, height // 2
            quads = [
                (0, 0, w2, h2),
                (w2, 0, width, h2),
                (0, h2, w2, height),
                (w2, h2, width, height),
            ]
            for quad in quads:
                draw.rectangle(quad, fill=create_random_color())
            return img

        def random_date_between(start_date, end_date):
            """
            Return a random date between two date objects (inclusive).
            """
            delta = (end_date - start_date).days
            random_day = random.randrange(delta + 1)
            return start_date + timedelta(days=random_day)

        start_dt = date(2025, 4, 1)
        end_dt   = date(2025, 7, 28)

        for i in range(1, 21):
            published_at = random_date_between(start_dt, end_dt)
            # Generate an English headline-like title
            title_en = fake.sentence(nb_words=5).rstrip(".")
            # Duplicate into other languages; admin can overwrite later
            title_fr = title_en
            title_rw = title_en
            title_sw = title_en

            # Generate a paragraph of “ad copy” (~80-120 words)
            paragraphs = fake.paragraphs(nb=2)
            content_en = " ".join(paragraphs)
            content_fr = content_en
            content_rw = content_en
            content_sw = content_en

            advert = Advertisement(
                published_at = published_at,
                title_en     = title_en,
                title_fr     = title_fr,
                title_rw     = title_rw,
                title_sw     = title_sw,
                content_en   = content_en,
                content_fr   = content_fr,
                content_rw   = content_rw,
                content_sw   = content_sw,
            )
            advert.save()  # initial save to get ID for slug-based image path

            # Create and save banner image
            img = create_banner_image(1200, 600)
            slug = slugify(title_en)
            filename = f"{slug}_{published_at.isoformat()}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)

            # Store the image path relative to MEDIA_ROOT
            advert.image = f"advertisements/{filename}"
            advert.save()

        self.stdout.write(self.style.SUCCESS("✅ 20 fake Advertisement entries created."))
