from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from business.models import Business


@receiver(post_save, sender=User)
def create_business_for_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Business.objects.get_or_create(owner=instance, defaults={"name": "My Business"})
