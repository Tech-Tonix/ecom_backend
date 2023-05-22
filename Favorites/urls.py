from rest_framework import routers
from . import views
from rest_framework_nested import routers
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register('favorites', views.FavoritesViewSet,basename='favorites')

urlpatterns = router.urls +[
    path('add-favorites/',views.AddFavoriteViewSet.as_view()),
    path('delete-favorites/<int:id>/', views.FavoritesViewSet.as_view({'delete':'destroy'})),
]