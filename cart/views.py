from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from django.contrib.auth.decorators import login_required
from book.models import Book
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from .models import *
from orders.models import OrderForm


# Create your views here.
def cart_detail(request, ):
    cart = Cart.objects.filter(user_id=request.user.id)
    form = OrderForm()
    total = 0
    for p in cart:
        total += p.product.price * p.quantity
    return render(request, 'shopping.html', {'cart': cart, 'total': total, 'form': form})


@login_required(login_url='accounts:login')
def cart_add(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        book = Book.objects.get(id=id)
        form = CartForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data['quantity']
            shop, created = Cart.objects.get_or_create(user_id=request.user.id, product=book)
            shop.quantity += info
            shop.save()
            messages.success(request, 'به سبد خرید اضافه شد', 'success')
        return redirect(url)


@login_required(login_url='accounts:login')
def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    messages.success(request, 'از سبد خرید حذف شد', 'success')
    return redirect(url)


def add_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    product = Book.objects.get(id=cart.product.id)
    if product.Inventory > cart.quantity:
        cart.quantity += 1
    cart.save()
    return redirect(url)


def remove_single(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)
