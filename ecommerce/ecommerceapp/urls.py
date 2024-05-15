from django.urls import path, include
from rest_framework import routers

from ecommerceapp import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('stores', views.StoreViewSet, basename='stores')
router.register('products', views.ProductViewSet, basename='products')
router.register('orders', views.OrderViewSet, basename='orders')
router.register(r'place-order', views.PlaceOrderViewSet, basename='place-order')
router.register(r'comments', views.CommentViewSet, basename='comments')
urlpatterns = [
    path('', include(router.urls))
]
