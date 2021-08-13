from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser


# Create your models here.

class MyUser(BaseUserManager):

    def user(self, email, username, password, **other_field):
        if not email:
            raise ValueError("ایمیل معتبر نیست")

        user = self.model(email=email, username=username, password=password, **other_field)
        user.save()
        return user


class BaseUser(AbstractBaseUser):
    user_name = models.CharField(max_length=150, unique=True)
    phone_no = models.IntegerField(null=False, blank=False)
    Postal_code = models.IntegerField(default=0)
    email = models.EmailField(max_length=200)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.user_name

class Address(models.Model):
    Postal_code = models.ForeignKey('account.BaseUser', on_delete=models.CASCADE, related_name='ads')
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
