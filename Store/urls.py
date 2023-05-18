from rest_framework import routers
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('carts', views.CartViewSet)
router.register('products', views.ProductsViewSet, basename='products')
router.register('Categories', views.CategoryViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + carts_router.urls