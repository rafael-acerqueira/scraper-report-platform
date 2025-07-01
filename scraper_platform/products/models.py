from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title