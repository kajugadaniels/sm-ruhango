import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from base.models import Homily

class Command(BaseCommand):
    help = "Generate 50 fake Homily entries with images"

    def handle(self, *args, **options):
        fake = Faker()
        output_dir = os.path.join(settings.MEDIA_ROOT, "homilies")
        os.makedirs(output_dir, exist_ok=True)

        def create_random_color():
            return tuple(random.randint(0, 255) for _ in range(3))

        def create_random_color_image(width, height):
            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)
            w2, h2 = width // 2, height // 2
            coords = [
                (0, 0, w2, h2),
                (w2, 0, width, h2),
                (0, h2, w2, height),
                (w2, h2, width, height),
            ]
            for coord in coords:
                draw.rectangle(coord, fill=create_random_color())
            return img

        def generate_christian_content():
            intro = (
                "Dear brothers and sisters in Christ, grace and peace be unto you. "
                "Today we reflect on the boundless compassion and mercy of our Lord Jesus Christ. "
                "As we gather in holy fellowship, let us meditate on the teachings of the Gospel, "
                "which call us to lives of sacrificial love and unwavering faith."
            )
            paras = fake.paragraphs(nb=3)
            return " ".join([intro] + paras)

        def ensure_word_count(text, min_words=500):
            words = text.split()
            while len(words) < min_words:
                words += fake.paragraph(nb_sentences=5).split()
            return " ".join(words)

        for i in range(1, 51):
            published_at = fake.date_between(start_date='-1y', end_date='today')
            title_en = fake.sentence(nb_words=6)
            content_en = ensure_word_count(generate_christian_content(), 500)

            # For now, duplicate English into other languages
            homily = Homily(
                published_at=published_at,
                title_en=title_en,
                title_fr=title_en,
                title_rw=title_en,
                title_sw=title_en,
                content_en=content_en,
                content_fr=content_en,
                content_rw=content_en,
                content_sw=content_en,
            )

            # generate and save image
            img = create_random_color_image(1200, 800)
            filename = f"homily_{i}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)
            homily.image = f"homilies/{filename}"

            homily.save()

        self.stdout.write(self.style.SUCCESS("Successfully generated 50 Homily entries."))
