from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('carts', views.CartViewSet)
router.register('products', views.ProductsViewSet, basename='products')
router.register('Categories', views.CategoryViewSet)

urlpatterns = router.urls