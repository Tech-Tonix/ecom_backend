from .models import  Category, Product, CartItem  , Order , OrderItem,ProductImage
from rest_framework import serializers
from core.models import CustomUser
from django.db import transaction
from Reviews.serializers import *


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')



class ProductSerializer(serializers.ModelSerializer):
    categories_title= serializers.CharField(source = 'categories.title',read_only = True)
    reviews = ReviewSerializer(many=True,read_only = True)
    images = ProductPhotoSerializer(many=True,required=False)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description','color','size','images','image_urls',
                  'unit_price', 'categories','categories_title','reviews','inventory']



# class ClothesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Clothes
#         fields = ['id', 'name', 'description','size','color', 
#                    'unit_price', 'categories','categories_title','image','reviews']
        

class SimpleProductSerializer(serializers.ModelSerializer):
    images = ProductPhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','name', 'unit_price','color','size','images']



class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'title', 'products']





#####################################################CART#########################################################



class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_product_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()


    def get_total_product_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    

    class Meta:
        model = CartItem
        fields = ['product', 'quantity' ,'total_product_price','total_price']

    def get_total_price(self, cart_item:CartItem):
        cart_items = CartItem.objects.filter(customer_id=cart_item.customer_id)
        return sum(item.quantity * item.product.unit_price for item in cart_items)

    
    def update(self,instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
    






class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


    class Meta:
        model = CartItem
        fields = [ 'product_id', 'quantity']





################################################ORDERS############################################################

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','product','quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id','customer', 'items' ,'total_amount','placed_at','status','tracking_number')



# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = ('customer', 'items' ,'total_amount','placed_at','status','tracking_number')

