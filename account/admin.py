from django.contrib import admin
from .models import Address, BaseUser, Customer, Employee, Admin, Profile


# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'postal_code']
    list_filter = ['postal_code']
    search_fields = ['postal_code', 'user', 'city']


admin.site.register(Address, AddressAdmin)


# admin.site.register(BaseUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
    list_filter = ['user']
    search_fields = ['user', 'phone']


admin.site.register(Profile, ProfileAdmin)


@admin.register(Admin)
class Admin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['email']

    def get_queryset(self, request):
        return BaseUser.objects.all()


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['email']

    def get_queryset(self, request):
        return BaseUser.objects.filter(is_staff=False)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['email']

    def get_queryset(self, request):
        return BaseUser.objects.filter(is_staff=True)
