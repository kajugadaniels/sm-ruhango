import os
import random
from datetime import timedelta, date, time as dtime
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from django.utils.text import slugify
from base.models import Event

class Command(BaseCommand):
    help = "Generate 30 fake Event entries with images"

    def handle(self, *args, **options):
        fake = Faker()
        output_dir = os.path.join(settings.MEDIA_ROOT, "events")
        os.makedirs(output_dir, exist_ok=True)

        def create_random_color():
            return tuple(random.randint(0, 255) for _ in range(3))

        def create_color_mosaic(width, height):
            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)
            w2, h2 = width // 2, height // 2
            quadrants = [
                (0, 0, w2, h2),
                (w2, 0, width, h2),
                (0, h2, w2, height),
                (w2, h2, width, height),
            ]
            for quad in quadrants:
                draw.rectangle(quad, fill=create_random_color())
            return img

        def generate_event_description(title, event_date):
            intro = (
                f"Join us for the {title} on {event_date.strftime('%B %d, %Y')}. "
                "This event brings together our community in faith and fellowship, "
                "offering spiritual nourishment and uplifting worship. "
            )
            paras = fake.paragraphs(nb=2)
            text = intro + " ".join(paras)
            words = text.split()
            while len(words) < 100:
                words += fake.paragraph(nb_sentences=3).split()
            return " ".join(words)

        BIBLE_TOPICS = [
            "the Good Samaritan", "the Prodigal Son", "the Beatitudes",
            "the Resurrection", "the Lord's Prayer", "the Ten Commandments"
        ]

        EVENT_TEMPLATES = [
            "Community Prayer Gathering",
            "Youth Faith Retreat",
            "Bible Study: {}",
            "Charity Outreach Program",
            "Adoration and Praise Night",
            "Family Worship Service",
            "Lenten Reflection Seminar",
            "Easter Vigil Mass",
            "Christmas Carol Celebration",
            "Healing Service and Prayers"
        ]

        for i in range(30):
            event_date = fake.date_between(start_date="today", end_date="+1y")
            tmpl = random.choice(EVENT_TEMPLATES)
            if "{}" in tmpl:
                topic = random.choice(BIBLE_TOPICS)
                title_en = tmpl.format(topic)
            else:
                title_en = tmpl

            hour = random.randint(8, 18)
            start = dtime(hour, random.choice([0, 15, 30, 45]))
            end_hour = hour + 1 if hour < 23 else 23
            end = dtime(end_hour, random.choice([0, 15, 30, 45]))

            desc_en = generate_event_description(title_en, event_date)

            event = Event(
                event_date=event_date,
                start_time=start,
                end_time=end,
                title_en=title_en,
                title_fr=title_en,
                title_rw=title_en,
                title_sw=title_en,
                description_en=desc_en,
                description_fr=desc_en,
                description_rw=desc_en,
                description_sw=desc_en,
            )
            event.save()  # initial save to generate slug

            img = create_color_mosaic(1200, 800)
            filename = f"event_{slugify(title_en)}_{event_date.isoformat()}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)

            event.image = f"events/{filename}"
            event.save()

        self.stdout.write(self.style.SUCCESS("Successfully generated 30 fake Event entries."))