from django.db import models
from business.models import Business


class GalleryImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.caption or f"Image {self.pk}"
