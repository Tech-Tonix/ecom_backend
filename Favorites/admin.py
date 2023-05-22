from django.contrib import admin
from .models import FavoritesItem , Favorites

admin.site.register(Favorites)
admin.site.register(FavoritesItem)

