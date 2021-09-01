from django.db import models
from account.models import BaseUser, Address
from book.models import Book
from django.forms import ModelForm


class Ordering(models.Model):
    STATUS = [('done', 'Done'), ('in_process', 'In_process'), ('in_basket', 'In_basket')]
    user_id = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user_id', null=True)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='In_basket')
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=3000, null=True, blank=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.status

    def get_price(self):
        total = sum(i.price() for i in self.order.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class ShoppingCart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True, related_name='order_item')
    order = models.ForeignKey(Ordering, on_delete=models.DO_NOTHING, null=True, related_name='order')
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def price(self):
        return self.book.total_price * self.book.Inventory


class OrderForm(ModelForm):
    class Meta:
        model = Ordering
        fields = ['address', 'first_name', 'last_name']


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.PositiveIntegerField()
