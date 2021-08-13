from django.db import models
# Create your models here.
from account.models import BaseUser

class Ordering(models.Model):
    user_id = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='user_id', null=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.PositiveBigIntegerField(default=0)
    number_shop = models.IntegerField(default=0)

class ShoppingCart(models.Model):
    shop_id = models.ForeignKey(Ordering, on_delete=models.DO_NOTHING, null=True)
    user_id = models.ForeignKey('account.BaseUser', on_delete=models.DO_NOTHING, null=True)
    unit_price = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    name_book = models.CharField(max_length=50, null=True)
