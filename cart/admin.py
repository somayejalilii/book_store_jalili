from django.contrib import admin
from cart.models import Cart


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['quantity']


admin.site.register(Cart, CartAdmin)
# admin.site.register(OrderCart)
# admin.site.register(Address)
# admin.site.register(Coupon)
