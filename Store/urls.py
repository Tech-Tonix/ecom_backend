from rest_framework import routers
from . import views
from rest_framework_nested import routers
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register('carts', views.CartItemViewSet,basename='carts')
router.register('products', views.ProductsViewSet, basename='products')
router.register('Categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls +[
    path('add-cart/',views.AddToCartViewSet.as_view()),
    path('delete-cartitem/<int:id>/',views.CartItemViewSet.as_view({'delete':'destroy'})),
    path('update-cartitem/<int:id>/',views.CartItemViewSet.as_view({'put':'update'})),
    path('orders/delete/<int:id>/', views.OrderViewSet.as_view({'delete':'destroy'})),
    path('orders/update/<int:order_id>/<int:order_item_id>/', views.OrderViewSet.as_view({'put': 'update'})),
    path('orders/delete-orderitem/<int:order_id>/<int:order_item_id>/', views.OrderItemViewset.as_view({'delete': 'destroy'})),
    path('order-tracking/', views.OrderTrackingViewset.as_view({'get': 'list'}), name='order-tracking'),


]