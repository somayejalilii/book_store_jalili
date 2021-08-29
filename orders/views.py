from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from cart.models import Cart
from account.models import BaseUser

# Create your views here.
def home_page(request):
    return render(request, 'base.html')


def order_detail(request, id):
    order = Ordering.objects.get(id=id)
    return render(request, 'orders.html', {'order': order})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Ordering.objects.create(first_name=['first_name'],
                                            last_name=['last_name'])
            cart = Cart.objects.filter(user_id=request.user.id)
            for cart in cart:
                ShoppingCart.objects.create(order_id=order.id, user_id=request.user.id, book_id=cart.product_id)
            Cart.objects.filter(user_id=request.user.id).delete()
            messages.success(request, 'سفارش شما ایجاد شد')
            return redirect('orders:order_detail', order.id)