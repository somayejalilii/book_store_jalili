from django.db import models
# Create your models here.
from account.models import BaseUser
from book.models import Book


class Ordering(models.Model):
    STATUS = [('done', 'Done'), ('in_process', 'In_process'), ('in_basket', 'In_basket')]
    user_id = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user_id', null=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.PositiveBigIntegerField(default=0)
    number_shop = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='In_basket')


class ShoppingCart(models.Model):
    shop_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING, null=True)
    user_id = models.ForeignKey(Ordering, on_delete=models.DO_NOTHING, null=True)
    number = models.IntegerField()
