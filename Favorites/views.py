from rest_framework import viewsets , status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.response import Response
from Store.models import Product
from rest_framework import generics


class FavoritesViewSet(viewsets.ViewSet):
    serializer_class = FavoritesSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get','delete']

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Favorites.objects.all()

        if user.is_authenticated:
            return Favorites.objects.filter(customer_id=user.id)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request,):
        user = self.request.user
        queryset = self.get_queryset()
        favorite = Favorites.objects.filter(customer_id=user.id)
        favorite_items = favorite.FavoriteItems.all()  # Retrieve all favorite items of the favorite
        serializer = FavoritesItemSerializer(favorite_items, many=True)  # Serialize the favorite items
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        favoriteItem_id = kwargs['id']
        favoriteitem = FavoritesItem.objects.get(id=favoriteItem_id, Favorites__customer=user)

        if not FavoritesItem.objects.filter(id=favoriteItem_id).exists():
            return Response(
                {'error': 'this item does not exist in your wishlist'},
                status=status.HTTP_404_NOT_FOUND
            )
        favoriteitem.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class AddFavoriteViewSet(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesItemSerializer
    queryset = FavoritesItem.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data.get('product_id')

        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': 'Associated product does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        product = Product.objects.get(id=product_id)

        favorites = Favorites.objects.filter(customer=user).first()

        if not favorites:
            # Create new favorites if it doesn't exist
            favorites = Favorites.objects.create(customer=user) 


        if FavoritesItem.objects.filter(Favorites=favorites, product=product).exists():
            return Response(
                {'error': 'Product already in favorites.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        favorite_item = FavoritesItem.objects.create(
            Favorites=favorites,
            product=product,
        )
        
        serializer = self.get_serializer(favorite_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    




