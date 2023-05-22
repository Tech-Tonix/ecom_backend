from .models import Favorites, FavoritesItem
from rest_framework import serializers


class FavoritesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritesItem
        fields=('product',)


class FavoritesSerializer(serializers.ModelSerializer):
    favorite_items = FavoritesItemSerializer(many=True,read_only=True)

    class Meta :
        model = Favorites
        fields= ('customer','favorite_items')
    