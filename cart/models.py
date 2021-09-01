from django.db import models

from account.models import BaseUser
from book.models import Book
from django.core.validators import MaxValueValidator, MinValueValidator
from book.models import *
from orders.models import Ordering
from django.forms import ModelForm


class Cart(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.user.username


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

