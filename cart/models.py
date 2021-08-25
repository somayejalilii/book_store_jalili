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

# class CartItem(models.Model):
#     cart_id = models.CharField(max_length=50)
#     date_added = models.DateTimeField(auto_now_add=True)
#     quantity = models.IntegerField(default=1)
#     books = models.ForeignKey('book.Book', unique=False, on_delete=models.CASCADE, )
#
#     class Meta:
#         db_table = 'cart_items'
#         ordering = ['date_added']
#
#     def total(self):
#         return self.quantity * self.books.price
#
#     def name(self):
#         return self.books.name
#
#     def price(self):
#         return self.books.price
#
#     # def get_absolute_url(self):
#     #     return self.books.get_absolute_url()
#
#     def augment_quantity(self, quantity):
#         self.quantity = self.quantity + int(quantity)
#         self.save()
#
#
# class OrderCart(models.Model):
#     customer = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     order_key = models.CharField(max_length=200)
#     billing_status = models.BooleanField(default=False)
#     updated = models.DateTimeField(auto_now=True)
#     paid = models.BooleanField(default=False)
#     discount = models.IntegerField(blank=True, null=True, default=None)
#
#     def __str__(self):
#         return f'{self.customer}  {self.id}'
#
#     class Meta:
#         ordering = ('-created',)
#
#     def get_total_price(self):
#         total = sum(i.get_cost() for i in self.item.all())
#         if self.discount:
#             discount_price = (self.discount / 100) * total
#             return int(total - discount_price)
#         return total
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Ordering, on_delete=models.CASCADE, related_name='item')
#     books = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_item')
#     quantity = models.SmallIntegerField(default=1)
#     price = models.IntegerField()
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity
#
#
# class Address(models.Model):
#     customer = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)
#     # order = models.ForeignKey(OrderCart, on_delete=models.SET_NULL, null=True)
#     city = models.CharField(max_length=200, null=False)
#     post_id = models.IntegerField(null=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#
# class Coupon(models.Model):
#     code = models.CharField(max_length=30, unique=True)
#     from_date = models.DateTimeField()
#     to_date = models.DateTimeField()
#     discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
#     active = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.code
