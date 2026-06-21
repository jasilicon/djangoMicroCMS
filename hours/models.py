from django.db import models
from business.models import Business


class BusinessHour(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="business_hours")
    day = models.IntegerField(choices=DAY_CHOICES)
    is_closed = models.BooleanField(default=False)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, help_text="e.g. By appointment only")

    class Meta:
        unique_together = ("business", "day")
        ordering = ["day"]

    def __str__(self):
        return f"{self.get_day_display()}: {self.open_time}-{self.close_time}" if not self.is_closed else f"{self.get_day_display()}: Closed"
