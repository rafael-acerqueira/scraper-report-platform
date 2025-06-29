from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
