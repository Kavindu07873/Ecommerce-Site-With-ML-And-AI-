from django.contrib import admin
from .models import Cart ,CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_addes')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')


admin.site.register(Cart , CartAdmin)

admin.site.register(CartItem ,CartItemAdmin)
