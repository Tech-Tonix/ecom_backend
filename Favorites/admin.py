from django.contrib import admin
from .models import FavoritesItem 

# admin.site.register(FavoritesItem)
class FavoritesItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'created_at']
    list_filter = ['customer', 'created_at']
    search_fields = ['customer__email', 'product__name']

admin.site.register(FavoritesItem, FavoritesItemAdmin)
