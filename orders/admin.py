from django.contrib import admin
from .models import Ordering, ShoppingCart, Coupon


# Register your models here.
class ShoppingInline(admin.TabularInline):
    model = ShoppingCart
    readonly_fields = ['user', 'book', 'number', 'price']


class OrderingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date', 'address', 'get_price','code')
    inlines = [ShoppingInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'discount', 'active']


admin.site.register(Ordering, OrderingAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Coupon, CouponAdmin)
