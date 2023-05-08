from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('carts', views.CartViewSet)
router.register('products', views.ProductsViewSet, basename='products')
router.register('products/<int:id>/', views.ProductDetail, basename='Product')
router.register('Categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls