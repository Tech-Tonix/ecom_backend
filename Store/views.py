from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import viewsets , status
from rest_framework.response import Response
from .models import *
from Store.serializers import *
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework import generics
import django_filters.rest_framework as  filters
from rest_framework.filters import SearchFilter , OrderingFilter
from .filter import *
from rest_framework import permissions
from .permissions import CanModifyOrderStatus


from datetime import timedelta, datetime , timezone
from .utils import recalculate_order_total , remove_quantity_from_inventory , update_quantity_from_inventory, re_put_quantity_to_inventory, member_club_reduction
from django.db import transaction



class ProductsViewSet(viewsets.ModelViewSet):

    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name','unit_price','categories__title','promotions__discount']
    order_fields = ['name','unit_price','promotions__discount','inventory']

    def get_permissions(self): 
        if self.request.method in ['PATCH', 'DELETE','POST','PUT']: #only the admin can update or delete the product
            return [IsAdminUser()]
        return []

    def get_queryset(self):
        return Product.objects.filter(inventory__gt=0)


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    

class ProductDetail(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


#######################################################################################################################

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(categories_id=kwargs['pk']):
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    

#####################################################################################################################

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'delete','put']
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return CartItem.objects.all()

        if user.is_authenticated:
            return CartItem.objects.filter(customer_id=user.id)
        


        
    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        queryset = CartItem.objects.filter(customer_id=user.id)
        
        product_id = kwargs['id']
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'Associated product does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        cart_item= queryset.filter(product_id=product_id).first()
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    

    def update(self, request, *args, **kwargs):
        user = self.request.user

        queryset = CartItem.objects.filter(customer_id=user.id)
        product_id = kwargs['id']
        if not Product.objects.filter(id=product_id).exists():
          return Response(
            {'error': 'Associated product does not exist.'},
            status=status.HTTP_404_NOT_FOUND
        )
        cart_item = queryset.filter(product_id=product_id).first()
        if cart_item is None:
          return Response(
            {'error': 'Associated product does not exist in the cart.'},
            status=status.HTTP_404_NOT_FOUND
        )

        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

    # Update the quantity
        quantity = serializer.validated_data.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()

        return Response(serializer.data)



class AddToCartViewSet(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddCartItemSerializer
    queryset = CartItem.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        # product_id = kwargs['id']
        product_id = request.data.get('product_id')
        if not Product.objects.filter(id=product_id).exists():
         return Response(
            {'error': 'Associated product does not exist.'},
            status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        user = request.user
        cart_item , created = CartItem.objects.get_or_create(
            customer=user,
            product=product,
            defaults={'quantity':quantity}
        )

        if not created:
            cart_item.quantity +=quantity
            cart_item.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)




###########################################################ORDER############################################################

class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'get','put','delete']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        if user.is_authenticated:
            return Order.objects.filter(customer_id=user.id)

   
        

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
    

    def create(self, request,*args, **kwargs):
        user = self.request.user
        cart_items = CartItem.objects.filter(customer=user)
 
        if not cart_items.exists():
            return Response(
                {'error': 'No items found in the cart.'},
                status=status.HTTP_400_BAD_REQUEST
            )      


        for cart_item in cart_items:
          if cart_item.quantity > cart_item.product.inventory:
              return Response(
                {'error': f"Insufficient inventory for product '{cart_item.product.name}'."},
                status=status.HTTP_400_BAD_REQUEST
              )

        total_amount = sum(item.product.unit_price * item.quantity for item in cart_items)

        order = Order.objects.create(
            customer=user,
            total_amount=total_amount,
        )

        # archived_order = ArchivedOrder.objects.create(
        #     customer=user,
        #     total_amount=order.total_amount,
        # ) 

        with transaction.atomic():
         for cart_item in cart_items:
            remove_quantity_from_inventory(cart_item) 
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

            # ArchivedOrderItems.objects.create(
            #  archived_order=order,
            #  product=cart_item.product,
            #  quantity=cart_item.quantity,
            # ) 
         cart_items.delete()
        member_club_reduction(user,order)
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        order_id = kwargs['id']

        order=Order.objects.get(id=order_id)

        if not Order.objects.filter(id=order_id).exists():
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        current_time = datetime.now(timezone.utc)

        time_difference = current_time - order.placed_at

        if time_difference > timedelta(hours=24):
            return Response(
                {'error': 'The deletion window for this order has expired.'},
                status=status.HTTP_403_FORBIDDEN
            )
 
        order_items=OrderItem.objects.filter(order=order)
        for order_item in order_items:
          re_put_quantity_to_inventory(order_item)
          order_item.delete()

        order.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


    def update(self, request, *args, **kwargs):

        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        try:
            order_item_id = kwargs['order_item_id']
            order_item = OrderItem.objects.get(id=order_item_id, order_id=order_id)


        except (KeyError, OrderItem.DoesNotExist):
             return Response(
                {'error': 'Order item not found.'},
                status=status.HTTP_404_NOT_FOUND
             )
        
        current_time = datetime.now(timezone.utc)

        time_difference = current_time - order.placed_at

        if time_difference > timedelta(hours=24):
            return Response(
                {'error': 'The deletion window for this order has expired.'},
                status=status.HTTP_403_FORBIDDEN
            )

        quantity = request.data.get('quantity')
        
        if quantity is None:
              return Response(
                 {'error': 'Quantity parameter is required.'},
                 status=status.HTTP_400_BAD_REQUEST
                 )
        try:
             quantity = int(quantity)
             if quantity < 0:
               return Response(
                  {'error': 'Quantity must be a non-negative integer.'},
                  status=status.HTTP_400_BAD_REQUEST
              )
         
             
        except ValueError:
              return Response(
               {'error': 'Invalid quantity value.'},
               status=status.HTTP_400_BAD_REQUEST
              )
        update_quantity_from_inventory(order_item,quantity)
        
        order_item.quantity= quantity

        order_item.save()

        recalculate_order_total(order)

        serializer = OrderSerializer(order_item.order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrderItemViewset(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
    
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)

        try:
            order_item_id = kwargs['order_item_id']
            order_item = OrderItem.objects.get(id=order_item_id, order_id=order_id)


        except (KeyError, OrderItem.DoesNotExist):
             return Response(
                {'error': 'Order item not found.'},
                status=status.HTTP_404_NOT_FOUND
             )
        current_time = datetime.now(timezone.utc)

        time_difference = current_time - order.placed_at

        if time_difference > timedelta(hours=24):
            return Response(
                {'error': 'The deletion window for this order has expired.'},
                status=status.HTTP_403_FORBIDDEN
            )
      
        order_item.delete()
        recalculate_order_total(order)

        return Response(status=status.HTTP_204_NO_CONTENT)




class OrderTrackingViewset(viewsets.ViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get','put']

    def get_permissions(self): 
        if self.request.method in ['PUT']:
            return [IsAdminUser(),CanModifyOrderStatus]
        return [IsAuthenticated()]
       
    
    def list(self, request, *args, **kwargs):
        tracking_number = request.GET.get('tracking_number')
        if tracking_number:
            order = Order.objects.filter(tracking_number=tracking_number).first()
            if order:
                serializer = self.serializer_class(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Tracking number not provided'}, status=status.HTTP_400_BAD_REQUEST)


    


