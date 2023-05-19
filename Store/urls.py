from rest_framework import routers
from . import views
from rest_framework_nested import routers
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register('carts', views.CartItemViewSet,basename='carts')
router.register('products', views.ProductsViewSet, basename='products')
router.register('Categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

# carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
# carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls +[
    path('add-cart/',views.AddToCartViewSet.as_view()),
    path('delete-cartitem/<int:id>/',views.CartItemViewSet.as_view({'delete':'destroy'})),
]