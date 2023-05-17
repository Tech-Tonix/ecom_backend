from django.shortcuts import render

from rest_framework import status,generics,mixins,viewsets
  #filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView ,RetrieveUpdateDestroyAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound , ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import ReviewSerializer
from .models import Review
from Store.models import Product


# Create your views here.
class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(product=pk)
    
class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        productlist = Product.objects.get(pk=pk)
        review_user = self.request.user
        print(review_user)
        review = Review.objects.filter(product=productlist,user=review_user)
        if review.exists():
            raise  ValidationError('you have already a review')
        if productlist.rating_nb == 0:
            # serializer.validated_data['rating'] or self.request.data['rating'] but with int
            productlist.rating_rv = serializer.validated_data['rating']
        else :
            productlist.rating_rv = (productlist.rating_rv + serializer.validated_data['rating'])/2
        productlist.rating_nb = productlist.rating_nb +1
            
        productlist.save()
        serializer.save(product=productlist,user=review_user  )
        
class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
