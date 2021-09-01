from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('<int:id>/', order_detail, name='order_detail'),
    path('create/', order_create, name='order_create'),
    path('coupone/<int:id>/', coupon_order, name='coupon'),
    path('request/<int:id><int:price>',send_request,name='request'),
    path('verify/',verify,name='verify'),
]
