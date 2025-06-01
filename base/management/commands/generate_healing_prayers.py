from django.core.management.base import BaseCommand
from base.models import HealingPrayer
from faker import Faker
from random import choice
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate fake Healing Prayers for the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generating 20 fake healing prayers
        for _ in range(20):
            title_en = fake.sentence(nb_words=5)
            title_fr = fake.sentence(nb_words=5)
            title_rw = fake.sentence(nb_words=5)
            title_sw = fake.sentence(nb_words=5)

            content_en = fake.text(max_nb_chars=500)
            content_fr = fake.text(max_nb_chars=500)
            content_rw = fake.text(max_nb_chars=500)
            content_sw = fake.text(max_nb_chars=500)

            # Generating a fake healing prayer image (you can also link it to real images if needed)
            image = None  # For simplicity, we can leave it as None or provide a random image path.

            # Create the healing prayer instance
            HealingPrayer.objects.create(
                title_en=title_en,
                title_fr=title_fr,
                title_rw=title_rw,
                title_sw=title_sw,
                content_en=content_en,
                content_fr=content_fr,
                content_rw=content_rw,
                content_sw=content_sw,
                image=image
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 20 fake Healing Prayers'))
