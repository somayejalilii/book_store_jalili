from django.contrib import admin
from .models import Address, BaseUser

# Register your models here.

@admin.register(BaseUser)
class CustomerAdmin(admin.ModelAdmin):
    fields = ('username',)

    def get_queryset(self, request):
        return BaseUser.objects.filter(is_staff=False)

    def get_queryset_employee(self, request):
        return BaseUser.objects.filter(is_staff=True)
