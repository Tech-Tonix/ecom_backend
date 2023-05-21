from .models import  Category, Product, CartItem  , Order , OrderItem
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from ecom_backend import settings
from core.models import CustomUser
from django.db import transaction
from Reviews.serializers import *
# from .signals import order_created



class ProductSerializer(serializers.ModelSerializer):
    categories_title= serializers.CharField(source = 'categories.title',read_only = True)
    reviews = ReviewSerializer(many=True,read_only = True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'inventory',
                  'unit_price', 'categories','categories_title','image','reviews']



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'unit_price']



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

# class OrderItemSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer()

#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity','unit_price']



# class OrderSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer(many=True)
#     class Meta:
#         model = Order
#         fields = [ 'customer', 'placed_at', 'payment_status', 'product']



# class CreateOrderSerializer(serializers.Serializer):
#     cart = serializers.IntegerField()

#     def validate_cart(self, cart_id): #test if the cart is empty oe deleted and raise validation error
#         if not CartItem.objects.filter(id=cart_id).exists():
#             raise serializers.ValidationError(
#                 'No cart with the given ID was found.')
#         if CartItem.objects.filter(cart_id=cart_id).count() == 0:
#             raise serializers.ValidationError('The cart is empty.')
#         return cart_id
    


#     def create(self, validated_data):
#       with transaction.atomic():
#         cart_id = validated_data['cart']
#         # Get the cart object
#         cart_items = CartItem.objects.get(id=cart_id)

#         customer = CustomUser.objects.get(
#             id=self.context['customer_id'])
#         order = Order.objects.create(customer=customer)

#         order_items = [
#             Order(
#                 order=order,
#                 product=item.product,
#             ) for item in cart_items
#         ]

#         # Bulk create order items
#         Order.objects.bulk_create(order_items)

#         # Delete cart items
#         cart_items.delete()

#         return order
    
    # def save(self, **kwargs):
    #     with transaction.atomic(): # we use it so the whole code works together and in case of internet cut the transaction doesn't stop in middle
    #         cart_id = self.validated_data['cart_id']

    #         customer = CustomUser.objects.get(
    #             id=self.context['customer_id'])
    #         order = Order.objects.create(customer=customer)

    #         cart_items = CartItem.objects \
    #             .select_related('product') \
    #             .filter(cart_id=cart_id)
    #         order_items = [
    #             Order(
    #                 order=order,
    #                 product=item.product,
    #             ) for item in cart_items
    #         ]
    #         Order.objects.bulk_create(order_items)

    #         CartItem.objects.filter(cart_id=cart_id).delete()

    #         return order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True,source='item')
    # status = Order

    class Meta:
        model = Order
        fields = ('customer', 'items', 'total_amount','placed_at','status')