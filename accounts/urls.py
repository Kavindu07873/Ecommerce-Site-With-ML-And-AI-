from django.conf import settings
from django.conf.urls.static import static
from . import views
# from .views import cart
from django.contrib import admin
from django.urls import path



urlpatterns = [
    path('register/',views.register  , name='register'),
    path('login/',views.login  , name='login'),
    path('logout/',views.logout  , name='logout'),
    path('dashboard/',views.dashboard  , name='dashboard'),
    path('',views.dashboard  , name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile , name='edit_profile')

    
] 
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

