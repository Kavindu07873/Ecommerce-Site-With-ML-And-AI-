
from . import views
from .views import cart
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('',views.cart  , name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart  , name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>',views.remove_cart  , name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>',views.remove_cart_item  , name='remove_cart_item'),


    # path('<slug:category_slug>/<slug:product_slug>/',views.product_details  , name='product_details'),
    path('checkout/' ,views.checkout ,name='checkout'),
    
] 
