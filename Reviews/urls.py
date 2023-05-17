from django.urls import path, include
from rest_framework import routers
from Reviews.views import *

# product-rating
urlpatterns = [
    path('products/<int:pk>/rating/', ReviewListAPIView.as_view(), name='rating-list'),
    path('products/<int:pk>/rating-create/', ReviewCreateAPIView.as_view(), name='rating-create'),
    path('products/rating/<int:pk>/',ReviewRetrieveUpdateDestroyAPIView.as_view(), name='rating-detail'),
]