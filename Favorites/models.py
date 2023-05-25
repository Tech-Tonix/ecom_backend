from django.db import models
from Store.models import Product
from core.models import CustomUser


class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorites ID: {self.id} - Customer: {self.customer.email}"

class FavoritesItem(models.Model):
    favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE,related_name='favorite_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='favorite_items')

    def __str__(self):
      return f"Favorite-item ID: {self.id} - Customer: {self.favorites.customer.email}"