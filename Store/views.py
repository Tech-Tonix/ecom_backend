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



class ProductsViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name','unit_price','categories__title','promotions__discount']
    order_fields = ['name','unit_price','promotions__discount','inventory']
    def get_permissions(self): 
        if self.request.method in ['PATCH', 'DELETE','POST','PUT']: #only the admin can update or delete the order
            return [IsAdminUser()]
        return []

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    

class ProductDetail(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(categories_id=kwargs['pk']):
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    






# class CartViewSet(CreateModelMixin,
#                   RetrieveModelMixin,
#                   DestroyModelMixin,
#                   GenericViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Cart.objects.prefetch_related('items', 'items__product').all()
#     serializer_class = CartItemSerializer




class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'delete','patch']

    # def get_serializer_class(self):
    #     if self.request.method == 'POST':
    #         return AddCartItemSerializer
    #     elif self.request.method == 'PATCH':
    #         return UpdateCartItemSerializer
    #     return CartItemSerializer

    
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



    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return CartItem.objects.all()

        if user.is_authenticated:
            return CartItem.objects.filter(customer_id=user.id)




class AddToCartViewSet(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddCartItemSerializer
    queryset = CartItem.objects.all()
    def create(self, request, *args, **kwargs):
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




#######################################################################################################################
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self): 
        if self.request.method in ['PATCH', 'DELETE']: #only the admin can update or delete the order
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'customer_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        # id = CustomUser.objects.only(
        #     'id').get(customer_id=id)
        # return Order.objects.filter(customer_id=id)
        
        id = self.request.GET.get('id')

        if id is not None:
          id = int(id)
          return Order.objects.filter(customer_id=id)

        return Order.objects.none()