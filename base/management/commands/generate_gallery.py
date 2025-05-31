import os
import random
from faker import Faker
from base.models import Gallery
from django.conf import settings
from PIL import Image, ImageDraw
from datetime import date, timedelta
from django.utils.text import slugify
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Generate 30 fake Gallery items with multilingual captions and images"

    def handle(self, *args, **options):
        fake = Faker()
        output_dir = os.path.join(settings.MEDIA_ROOT, "gallery")
        os.makedirs(output_dir, exist_ok=True)

        def create_random_color():
            return tuple(random.randint(0, 255) for _ in range(3))

        def create_mosaic_image(width, height):
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

        # Generate 30 items
        for i in range(1, 31):
            # Generate random captions
            caption_en = fake.sentence(nb_words=6).rstrip(".")
            caption_fr = caption_en
            caption_rw = caption_en
            caption_sw = caption_en

            gallery_item = Gallery(
                caption_en=caption_en,
                caption_fr=caption_fr,
                caption_rw=caption_rw,
                caption_sw=caption_sw,
            )
            gallery_item.save()  # save to get ID for slug

            # Create and save image
            img = create_mosaic_image(1200, 800)
            slug = slugify(caption_en[:50])
            filename = f"{slug}_{gallery_item.id}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)

            # Assign and save image field
            gallery_item.image = f"gallery/{filename}"
            gallery_item.save()

        self.stdout.write(self.style.SUCCESS("✓ Successfully generated 30 Gallery items."))
