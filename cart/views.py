from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from book.models import Book
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from .models import *


# Create your views here.
def cart_detail(request,):
    cart = Cart.objects.filter(user_id=request.user.id)
    total = 0
    for p in cart:
        total += p.product.price * p.quantity
    return render(request, 'shopping.html', {'cart': cart, 'total': total})

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
        return redirect(url)

def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)






