from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('update/', user_update, name='update'),
    path('logout/',user_logout,name='logout'),
    path('change/', change_password, name='change_password'),
    # path('login_phone/',phone,name='phone'),
    # path('veryfy/',verify,name='verify'),
    path('active/<uidb64>/<token>/',RegisterEmail.as_view(),name='active'),
    path('reset/',ResetPassword.as_view(),name='reset'),
    path('reset/done/',DonePassword.as_view(),name='reset_done'),
    path('confirm/<uidb64>/<token>/',password_reset_confirm.as_view(),name='password_reset_confirm'),
    path('confirm/done/',Complete.as_view(),name='complete'),
    path('favorite/<int:id>/',favorite,name='favorite'),
    path('history/',history,name='history'),
]
