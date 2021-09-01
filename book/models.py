from django.db import models
from django.urls import reverse
from account.models import BaseUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='books')
    author = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now=True,blank=True, null=True)
    Inventory = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='books', null=True, blank=True)
    total_price = models.PositiveIntegerField(blank=True, null=True)
    available = models.BooleanField(default=True,blank=True, null=True)
    favorite = models.ManyToManyField(BaseUser,blank=True,null=True,related_name='fa_user')
    is_favorite = models.BooleanField(null=True,blank=True,default=False)

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.price
        elif self.discount:
            total = (self.discount * self.price) / 100
            return int(self.price - total)
        return self.total_price
