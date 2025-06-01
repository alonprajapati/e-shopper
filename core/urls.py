from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('shop/',shop,name="shop"),
    path('contact/',contact, name='contact'),
    path('checkout/',checkout, name='checkout'),
    path('product_details/<int:id>',product_detail, name='product_detail'),
    # path("login/",log_in,name="log_in"),
    path('blog/',blog, name='blog'),
    path('blog-single/',blog_single, name='blog_single'),
    path('404/',error, name='error'),   
    # ////add to cart
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'), 
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
]
