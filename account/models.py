from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser


# Create your models here.

class MyUser(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('لطفا تنظیمات را در قسمت کارمندان درست کنید')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('لطفا تنظیمات را در قسمت ادمین درست کنیذ')
        return self.create_superuser(email, user_name, password, **other_fields)

    def user(self, email, username, password, **other_field):
        if not email:
            raise ValueError("ایمیل معتبر نیست")

        user = self.model(email=email, username=username, password=password, **other_field)
        user.save()
        return user


class BaseUser(AbstractBaseUser):
    user_name = models.CharField(max_length=150, unique=True)
    phone_no = models.IntegerField(null=False, blank=False)
    email = models.EmailField(max_length=200)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    # class Meta:
    #     proxy = True
    #     verbose_name = 'customer'
    #     verbose_name_plural = 'customers'
    #
    # class Meta1:
    #     proxy = True
    #     verbose_name = 'employee'
    #     verbose_name_plural = 'employees'

    def __str__(self):
        return self.user_name

class Address(models.Model):
    user = models.ForeignKey('account.BaseUser', on_delete=models.CASCADE, related_name='ads')
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    postal_code = models.IntegerField()
