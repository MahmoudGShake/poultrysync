from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet,export_orders_csv,index

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', index, name='index'),
    path('api/orders/export/', export_orders_csv, name='export-orders'),
    path('api/', include(router.urls)),
]
