
from . import views
from .views import store
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('',views.store  , name='store'),
    path('category/<slug:category_slug>/',views.store  , name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_details  , name='product_details'),
    path('search/' , views.search , name='search'),
    path('submit_review/<int:product_id>/', views.submit_review  , name ='submit_review')

] 
