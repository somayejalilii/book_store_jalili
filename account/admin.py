from django.contrib import admin
from .models import Address, BaseUser, Customer, Employee, Admin, Profile

# Register your models here.
admin.site.register(Address)


# admin.site.register(BaseUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']


admin.site.register(Profile, ProfileAdmin)


@admin.register(Admin)
class Admin(admin.ModelAdmin):

    def get_queryset(self, request):
        return BaseUser.objects.all()


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return BaseUser.objects.filter(is_staff=False)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return BaseUser.objects.filter(is_staff=True)
