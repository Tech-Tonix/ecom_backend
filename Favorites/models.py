from django.db import models
from Store.models import Product
from core.models import CustomUser


class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class FavoritesItem(models.Model):
    Favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='FavoriteItems')
