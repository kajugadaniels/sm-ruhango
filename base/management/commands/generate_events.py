# base/management/commands/generate_events.py

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
    help = "Generate 30 multilingual fake Event entries with images"

    def handle(self, *args, **options):
        # Initialize Faker for each locale (fallback to default when unsupported)
        fake_en = Faker()
        try:
            fake_fr = Faker('fr_FR')
        except Exception:
            fake_fr = fake_en
        try:
            fake_rw = Faker('rw_RW')
        except Exception:
            fake_rw = fake_en
        try:
            fake_sw = Faker('sw_KE')
        except Exception:
            fake_sw = fake_en

        output_dir = os.path.join(settings.MEDIA_ROOT, "events")
        os.makedirs(output_dir, exist_ok=True)

        def create_random_color():
            return tuple(random.randint(0, 255) for _ in range(3))

        def create_color_mosaic(width, height):
            img = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(img)
            w2, h2 = width // 2, height // 2
            quads = [(0,0,w2,h2), (w2,0,width,h2), (0,h2,w2,height), (w2,h2,width,height)]
            for quad in quads:
                draw.rectangle(quad, fill=create_random_color())
            return img

        def generate_description(fake_inst, title, edate, lang):
            # Handcrafted intros per language
            if lang == 'en':
                intro = (
                    f"Join us for the {title} on {edate.strftime('%B %d, %Y')}. "
                    "This event brings together our community in faith and fellowship, "
                    "offering spiritual nourishment and uplifting worship."
                )
            elif lang == 'fr':
                intro = (
                    f"Rejoignez-nous pour {title} le {edate.strftime('%d %B %Y')}. "
                    "Cet événement rassemble notre communauté dans la foi et la fraternité, "
                    "offrant une nourriture spirituelle et un culte édifiant."
                )
            elif lang == 'rw':
                intro = (
                    f"Duhure muri {title} ku itariki ya {edate.strftime('%d %B %Y')}. "
                    "Iki gikorwa gikusanya umuryango wacu mu kwizera no gusangira, "
                    "gitanga impanuro z’Imana n’ibikorwa by’ubusabane bubaka."
                )
            else:  # sw
                intro = (
                    f"Jiunge nasi katika {title} tarehe {edate.strftime('%d %B %Y')}. "
                    "Tukio hili linaunganisha jamii yetu katika imani na undugu, "
                    "likitoa lishe ya kiroho na ibada yenye kukuinua."
                )

            paras = fake_inst.paragraphs(nb=2)
            text = intro + " " + " ".join(paras)
            words = text.split()
            # Guarantee at least 100 words
            while len(words) < 100:
                words += fake_inst.paragraph(nb_sentences=3).split()
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
            # Pick a date within the next year
            event_date = fake_en.date_between(start_date="today", end_date="+1y")

            # Build English title (with occasional Bible topic)
            tmpl = random.choice(EVENT_TEMPLATES)
            if "{}" in tmpl:
                title_en = tmpl.format(random.choice(BIBLE_TOPICS))
            else:
                title_en = tmpl

            # Generate localized titles
            title_fr = fake_fr.sentence(nb_words=6).rstrip('.')
            title_rw = fake_rw.sentence(nb_words=6).rstrip('.')
            title_sw = fake_sw.sentence(nb_words=6).rstrip('.')

            # Random time slot
            hour = random.randint(8, 18)
            start = dtime(hour, random.choice([0,15,30,45]))
            end   = dtime(min(hour+1,23), random.choice([0,15,30,45]))

            # Generate rich descriptions
            desc_en = generate_description(fake_en, title_en, event_date, 'en')
            desc_fr = generate_description(fake_fr, title_fr, event_date, 'fr')
            desc_rw = generate_description(fake_rw, title_rw, event_date, 'rw')
            desc_sw = generate_description(fake_sw, title_sw, event_date, 'sw')

            # Create and save the Event instance (slug generated in model.save)
            event = Event(
                event_date=event_date,
                start_time=start,
                end_time=end,
                title_en=title_en,
                title_fr=title_fr,
                title_rw=title_rw,
                title_sw=title_sw,
                description_en=desc_en,
                description_fr=desc_fr,
                description_rw=desc_rw,
                description_sw=desc_sw,
            )
            event.save()

            # Generate and attach mosaic image
            img = create_color_mosaic(1200, 800)
            fn  = f"event_{slugify(title_en)}_{event_date.isoformat()}.jpg"
            path = os.path.join(output_dir, fn)
            img.save(path, quality=85)
            event.image = f"events/{fn}"
            event.save()

        self.stdout.write(self.style.SUCCESS("✅ Generated 30 multilingual Event entries."))

