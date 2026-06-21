from django.db import models
from business.models import Business


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("twitter", "X (Twitter)"),
        ("yelp", "Yelp"),
        ("tiktok", "TikTok"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
        ("whatsapp", "WhatsApp"),
        ("website", "Website"),
        ("other", "Other"),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    label = models.CharField(max_length=100, blank=True)
    url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.label or self.get_platform_display()
