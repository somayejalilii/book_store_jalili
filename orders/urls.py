from django.urls import path
from .views import *
app_name = 'orders'

urlpatterns = [
    path('<int:id>', order_detail, name='order_detail'),
    path('create/', order_create, name='order_create'),
]