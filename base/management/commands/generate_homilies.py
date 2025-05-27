import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from base.models import Homily

class Command(BaseCommand):
    help = "Generate 50 fake Homily entries with images and multilingual content"

    def handle(self, *args, **options):
        # Separate Faker instances for different locales
        fake_en = Faker('en_US')
        fake_fr = Faker('fr_FR')
        fake_rw = Faker()   # fallback for Kinyarwanda
        fake_sw = Faker()   # fallback for Kiswahili

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

        def ensure_word_count(text, min_words=500):
            words = text.split()
            while len(words) < min_words:
                # add more filler sentences
                words += fake_en.paragraph(nb_sentences=5).split()
            return " ".join(words)

        def generate_christian_content_en():
            intro = (
                "Dear brothers and sisters in Christ, grace and peace be unto you. "
                "Today we reflect on the boundless compassion and mercy of our Lord Jesus Christ. "
                "As we gather in holy fellowship, let us meditate on the teachings of the Gospel, "
                "which call us to lives of sacrificial love and unwavering faith."
            )
            paras = fake_en.paragraphs(nb=4)
            return " ".join([intro] + paras)

        def generate_christian_content_fr():
            intro = (
                "Chers frères et sœurs en Christ, que la grâce et la paix soient avec vous. "
                "Aujourd’hui, nous réfléchissons à la compassion et à la miséricorde infinies de notre Seigneur Jésus-Christ. "
                "Alors que nous nous rassemblons dans la sainte communion, méditons sur les enseignements de l’Évangile, "
                "qui nous appellent à mener une vie d’amour sacrificiel et de foi inébranlable."
            )
            paras = fake_fr.paragraphs(nb=4)
            return " ".join([intro] + paras)

        def generate_christian_content_rw():
            intro = (
                "Bavandimwe mu Kristu, umugisha n’amahoro by’Imana bijye bibana namwe. "
                "Uyu munsi twibuka imbabazi n’urukundo bidashira byacu Yesu Kristo. "
                "Mu rusengero, duhure mu gusenga no mu ndirimbo dusabira amahoro n’ubugorwa bw’Imana. "
                "Mwigire ku nyigisho z’Ivangeli zitubwira ku rukundo rudasaza n’ukwemera kudacogora."
            )
            paras = fake_rw.paragraphs(nb=4)
            return " ".join([intro] + paras)

        def generate_christian_content_sw():
            intro = (
                "Ndugu wapendwa katika Kristo, neema na amani ziwe nanyi. "
                "Leo tunafikiria juu ya huruma isiyo na kipimo ya Bwana wetu Yesu Kristo. "
                "Tukiakusanyika katika ibada ya pamoja, tuweze kutafakari mafundisho ya Injili, "
                "yanayosihi kuishi kwa upendo wa kujitoa na imani thabiti."
            )
            paras = fake_sw.paragraphs(nb=4)
            return " ".join([intro] + paras)

        for i in range(1, 51):
            published_at = fake_en.date_between(start_date='-1y', end_date='today')

            # Titles in each language
            title_en = fake_en.sentence(nb_words=6)
            title_fr = fake_fr.sentence(nb_words=6)
            title_rw = fake_rw.sentence(nb_words=6)
            title_sw = fake_sw.sentence(nb_words=6)

            # Content in each language, ensured ≥500 words
            content_en = ensure_word_count(generate_christian_content_en())
            content_fr = ensure_word_count(generate_christian_content_fr())
            content_rw = ensure_word_count(generate_christian_content_rw())
            content_sw = ensure_word_count(generate_christian_content_sw())

            # Instantiate and assign
            homily = Homily(
                published_at=published_at,
                title_en=title_en,
                title_fr=title_fr,
                title_rw=title_rw,
                title_sw=title_sw,
                content_en=content_en,
                content_fr=content_fr,
                content_rw=content_rw,
                content_sw=content_sw,
            )

            # Generate and save a random color-block image
            img = create_random_color_image(1200, 800)
            filename = f"homily_{i}.jpg"
            path = os.path.join(output_dir, filename)
            img.save(path, quality=85)
            homily.image = f"homilies/{filename}"

            homily.save()

        self.stdout.write(self.style.SUCCESS("✅ Generated 50 multilingual Homily entries with images."))
