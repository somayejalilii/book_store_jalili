from django.contrib import admin
from .models import Ordering, ShoppingCart


# Register your models here.
class ShoppingInline(admin.TabularInline):
    model = ShoppingCart
    readonly_fields = ['user', 'book', 'number']


class OrderingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date', 'address')
    inlines = [ShoppingInline]


admin.site.register(Ordering, OrderingAdmin)
admin.site.register(ShoppingCart)
