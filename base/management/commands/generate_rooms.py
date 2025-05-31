import os
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from PIL import Image, ImageDraw
from django.utils.text import slugify
from base.models import Amenity, Room, RoomImage

class Command(BaseCommand):
    help = "Generate 20 fake rooms, each with at least 4 images and random amenities"

    def handle(self, *args, **options):
        fake = Faker()

        # Ensure default amenities exist
        default_amenities = [
            "Free WiFi", "Air Conditioning", "Breakfast Included", "Parking", "Pool Access", "Gym Access", "Pet Friendly", "Room Service"
        ]
        if Amenity.objects.count() == 0:
            for amen_name in default_amenities:
                Amenity.objects.create(name=amen_name)
            self.stdout.write(self.style.SUCCESS("✔ Default amenities created."))

        amenities_qs = list(Amenity.objects.all())

        def create_random_image(width, height, dest_path):
            # Create a simple color mosaic image
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
                color = tuple(random.randint(0, 255) for _ in range(3))
                draw.rectangle(quad, fill=color)
            img.save(dest_path, format='JPEG', quality=85)

        # Generate 20 rooms
        for i in range(1, 21):
            title = f"{fake.word().capitalize()} {random.choice(['Room','Suite','Deluxe','Studio'])}"
            location = fake.city()
            description = "\n\n".join(fake.paragraphs(nb=3))
            price = round(random.uniform(50, 300), 2)

            room = Room(
                title=title,
                location=location,
                description=description,
                price_per_night=price,
            )
            room.save()  # slug is now set

            # Assign random 3-5 amenities
            num_amen = random.randint(3, 5)
            chosen = random.sample(amenities_qs, num_amen)
            room.amenities.set(chosen)

            # Create directory for images: MEDIA_ROOT/rooms/room_<slug>
            slug = slugify(room.title)
            img_dir = os.path.join(settings.MEDIA_ROOT, f"rooms/room_{slug}")
            os.makedirs(img_dir, exist_ok=True)

            # Generate 4 images per room
            for idx in range(1, 5):
                filename = f"image_{idx}.jpg"
                file_path = os.path.join(img_dir, filename)
                create_random_image(800, 600, file_path)

                # Save RoomImage pointing to relative path
                rel_path = f"rooms/room_{slug}/{filename}"
                room_image = RoomImage(
                    room=room,
                    image=rel_path,
                    alt_text=f"{room.title} image {idx}"
                )
                room_image.save()

            self.stdout.write(self.style.SUCCESS(f"✔ Created room '{room.title}' with 4 images and amenities."))

        self.stdout.write(self.style.SUCCESS("🎉 Successfully generated 20 rooms with images and amenities."))
