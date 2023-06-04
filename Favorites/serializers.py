from .models import  FavoritesItem
from rest_framework import serializers
from Store.serializers import SimpleProductSerializer , ProductSerializer


class FavoritesItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    class Meta:
        model = FavoritesItem
        fields=['product', 'customer',]

   

    
class AddFavoriteItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = FavoritesItem
        fields = ('product_id',)