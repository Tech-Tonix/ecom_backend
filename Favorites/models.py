from django.db import models
from core.models import Product


class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)




class FavoritesItem(models.Model):
    Favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
