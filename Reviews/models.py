from django.db import models
from django.conf import settings
from Store.models import Product
from core.models import *

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name + " rating's is " + str(self.rating)

