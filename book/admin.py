from django.contrib import admin
from book.models import Book, Category


# Register your models here.
# admin.site.register(Book)
# admin.site.register(Category)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    search_fields = ['name']
# class BookInstanceInline(admin.TabularInline):
#     model = Category
#
#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('name', 'author')
#     inlines = [BookInstanceInline]
