
from . import views
from django.contrib import admin
from django.urls import path



urlpatterns = [
    # path('',views.store  , name='store'),
    path('place_order/',views.place_order  , name='place_order'),
    path('payments/',views.payments  , name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),


] 
