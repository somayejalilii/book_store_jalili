from django.contrib import admin
from .models import Address, BaseUser

# Register your models here.
admin.site.register(BaseUser)
admin.site.register(Address)
