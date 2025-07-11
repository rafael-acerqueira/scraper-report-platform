from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ScraperLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    scraper_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    records = models.PositiveIntegerField(default=0)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.scraper_name}: {self.status}"