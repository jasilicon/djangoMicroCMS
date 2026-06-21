from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    about = models.TextField(blank=True)
    address = models.CharField(max_length=500, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    google_maps_embed_url = models.URLField(blank=True, verbose_name="Google Maps Embed URL")
    logo = models.ImageField(upload_to="businesses/logos/", blank=True)
    favicon = models.ImageField(upload_to="businesses/favicons/", blank=True)
    is_published = models.BooleanField(default=False, verbose_name="Site published")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "businesses"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SectionPublish(models.Model):
    SECTION_CHOICES = [
        ("hero", "Hero"),
        ("about", "About"),
        ("services", "Services"),
        ("gallery", "Gallery"),
        ("hours", "Business Hours"),
        ("contact", "Contact"),
        ("social", "Social Links"),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="section_publishes")
    section_slug = models.CharField(max_length=20, choices=SECTION_CHOICES)
    is_published = models.BooleanField(default=True)

    class Meta:
        unique_together = ("business", "section_slug")

    def __str__(self):
        return f"{self.business.name} - {self.get_section_slug_display()}"


class HeroImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="hero_images")
    image = models.ImageField(upload_to="businesses/hero/")
    alt_text = models.CharField(max_length=200, blank=True)
    cta_text = models.CharField(max_length=100, blank=True)
    cta_url = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.alt_text or f"Hero {self.pk}"


class SiteSetting(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="settings", null=True, blank=True)
    key = models.CharField(max_length=100)
    value = models.TextField(blank=True)

    class Meta:
        unique_together = ("business", "key")

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"
