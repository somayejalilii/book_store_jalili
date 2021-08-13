from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    author = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now=True)
    Inventory = models.IntegerField()
    price = models.PositiveBigIntegerField()

