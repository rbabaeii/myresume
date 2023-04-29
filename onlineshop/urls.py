from django.urls import path
from .views import *

app_name = 'onlineshop'

urlpatterns = [
    path('home-page/' , HomePage.as_view() , name='home-page'),
    path('products/all/' , ListProductView.as_view() , name='list-product'),
    path('product/detail/<str:pk>/' , ProductDetail.as_view() , name='product-detail'),
    path('product/add/<str:pk>/' ,AddProductView.as_view() , name='product-add'),
    path('product/remove/<str:pk>/' , RemoveProductView.as_view() , name='product-remove'),
    path('cart/detail/' , CartDetailView.as_view() , name='cart-detail'),
    path('order/detail/<str:pk>/' , OrderDetailView.as_view() , name='order-detail'),
    path('order/add/' , OrderCreationView.as_view() , name='order-add'),
    path('contact/' , ContactUsView.as_view() , name='contact'),
    path('order/pay/<str:pk>/' , PayOrder.as_view() , name='order-pay'),
    # path('order/verify/' , VerifyOrder.as_view() , name='order-verify'),
]
