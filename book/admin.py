from django.contrib import admin
from .models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_created', 'price', 'total_price', 'Inventory', 'available']
    list_filter = ('available',)
    search_fields = ['name', 'author']


admin.site.register(Book, BookAdmin)
