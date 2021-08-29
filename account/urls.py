from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('update/', user_update, name='update'),
    path('change/', change_password, name='change_password'),
    # path('login_phone/',phone,name='phone'),
    # path('veryfy/',verify,name='verify'),
]
