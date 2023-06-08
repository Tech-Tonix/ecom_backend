from django.shortcuts import render
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework import status,generics,mixins,viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView ,RetrieveUpdateDestroyAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound , ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import ReviewSerializer
from .models import Review
from Store.models import Product
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(product=pk)
    
class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def perform_create(self, serializer):
      
      pk = self.kwargs.get('pk')
      productlist = Product.objects.get(pk=pk)
      review_user = self.request.user
      print(review_user)
      review = Review.objects.filter(product=productlist, user=review_user)
      if review.exists():
        raise ValidationError('You have already submitted a review.')
    
      if 'rating' in serializer.validated_data:

         if productlist.rating_nb == 0:
            productlist.rating_rv = serializer.validated_data['rating']
         else:
            productlist.rating_rv = (productlist.rating_rv + serializer.validated_data['rating']) / 2
         productlist.rating_nb += 1
         productlist.save()

      serializer.save(product=productlist, user=review_user)

class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


    def perform_destroy(self, instance):
        user = self.request.user

        if instance.user != user:
            raise PermissionDenied("You are not allowed to delete this review.")

        instance.delete()
