from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from business.models import Business, SectionPublish
from services.models import ServiceCategory, Service
from hours.models import BusinessHour
from social.models import SocialLink


class Command(BaseCommand):
    help = "Seed the database with demo data for a restaurant"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="owner",
            defaults={"email": "owner@example.com", "is_staff": True},
        )
        if created:
            user.set_password("owner")
            user.save()

        business, _ = Business.objects.update_or_create(
            owner=user,
            defaults={
                "name": "Bella Italia Ristorante",
                "tagline": "Authentic Italian cuisine since 1998",
                "about": "<p>Welcome to <strong>Bella Italia</strong>, where tradition meets taste.</p><p>Our family recipes have been passed down through generations, bringing you the true flavors of Tuscany and Sicily.</p><p>We use only the freshest ingredients, imported Italian wines, and hand-made pasta.</p>",
                "address": "123 Main Street\nDowntown, CA 90210",
                "phone": "(555) 123-4567",
                "email": "hello@bellaitalia.example.com",
                "google_maps_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d387190.2799151706!2d-74.25987368715497!3d40.69767006353956!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNew+York%2C+NY!5e0!3m2!1sen!2sus!4v1563994345237!5m2!1sen!2sus",
                "is_published": True,
            },
        )

        for section_slug, _ in SectionPublish.SECTION_CHOICES:
            SectionPublish.objects.get_or_create(
                business=business, section_slug=section_slug,
                defaults={"is_published": True},
            )

        pasta, _ = ServiceCategory.objects.get_or_create(
            business=business, name="Pasta", defaults={"sort_order": 1},
        )
        Service.objects.get_or_create(
            category=pasta, name="Spaghetti Carbonara",
            defaults={"description": "Creamy egg sauce with pancetta and pecorino romano", "price": 18.99, "sort_order": 1},
        )
        Service.objects.get_or_create(
            category=pasta, name="Penne Arrabbiata",
            defaults={"description": "Spicy tomato sauce with garlic and fresh basil", "price": 15.99, "sort_order": 2},
        )
        Service.objects.get_or_create(
            category=pasta, name="Lasagna Classica",
            defaults={"description": "Layered pasta with bolognese, béchamel, and melted mozzarella", "price": 21.99, "sort_order": 3},
        )

        pizza, _ = ServiceCategory.objects.get_or_create(
            business=business, name="Pizza", defaults={"sort_order": 2},
        )
        Service.objects.get_or_create(
            category=pizza, name="Margherita",
            defaults={"description": "San Marzano tomatoes, fresh mozzarella, basil", "price": 16.99, "sort_order": 1},
        )
        Service.objects.get_or_create(
            category=pizza, name="Diavola",
            defaults={"description": "Spicy salami, chili flakes, mozzarella", "price": 19.99, "sort_order": 2},
        )

        drinks, _ = ServiceCategory.objects.get_or_create(
            business=business, name="Drinks", defaults={"sort_order": 3},
        )
        Service.objects.get_or_create(
            category=drinks, name="Espresso",
            defaults={"description": "Double shot espresso", "price": 3.50, "sort_order": 1},
        )
        Service.objects.get_or_create(
            category=drinks, name="Italian Wine - Glass",
            defaults={"description": "Ask your server for tonight's selection", "price": 12.00, "sort_order": 2},
        )

        days = [
            (0, "09:00", "22:00"),
            (1, "09:00", "22:00"),
            (2, "09:00", "22:00"),
            (3, "09:00", "22:00"),
            (4, "09:00", "23:00"),
            (5, "10:00", "23:00"),
            (6, "10:00", "21:00"),
        ]
        for day_num, open_t, close_t in days:
            import datetime
            BusinessHour.objects.get_or_create(
                business=business, day=day_num,
                defaults={"open_time": datetime.time.fromisoformat(open_t), "close_time": datetime.time.fromisoformat(close_t)},
            )

        SocialLink.objects.get_or_create(
            business=business, platform="facebook",
            defaults={"url": "https://facebook.com/bellaitalia", "sort_order": 1},
        )
        SocialLink.objects.get_or_create(
            business=business, platform="instagram",
            defaults={"url": "https://instagram.com/bellaitalia", "sort_order": 2},
        )
        SocialLink.objects.get_or_create(
            business=business, platform="yelp",
            defaults={"url": "https://yelp.com/bellaitalia", "sort_order": 3},
        )

        self.stdout.write(self.style.SUCCESS(f"Seeded business: {business.name}"))
        self.stdout.write(self.style.SUCCESS(f"Owner login: owner / owner"))
        self.stdout.write(self.style.SUCCESS(f"Admin login: admin / admin"))
