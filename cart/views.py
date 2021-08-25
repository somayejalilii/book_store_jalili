from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from book.models import Book
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from .models import *


# Create your views here.
def cart_detail(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    total = 0
    for p in cart:
        total += p.product.price * p.quantity
    return render(request, 'shopping.html', {'cart': cart, 'total': total})

def cart_add(request, id):
    url = request.META.get('HTTP_REFERER')
    book = Book.objects.get(id=id)
    # var_id = request.POST.get('select')
    data = Cart.objects.filter(user_id=request.user.id, id=id)
    if data:
        check = 'وجود دارد'
    else:
        check = 'وجود ندارد'
        if request.method == 'POST':
            form = CartForm(request.POST)
            # var_id = request.POST.get('select')
            if form.is_valid():
                info = form.cleaned_data['quantity']
                if check == 'وجود دارد':
                    shop = Cart.objects.get(user_id=request.user.id, id=id)
                    shop.quantity += info
                    shop.save()
                else:
                    Cart.objects.create(user_id=request.user.id, id=id, quantity=info)
            return redirect(url)

def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)






# @require_POST
# def cart_add(request, id):
#     cart = Cart(request)
#     book = get_object_or_404(Book, id=id)
#     form = CartAddForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(book=book, quantity=cd['quantity'])
#     return redirect('cart:detail')
#
#
# def remove_cart(request, book_id):
#     cart = Cart(request)
#     book = get_object_or_404(Book, id=book_id)
#     cart.remove(book)
#     return redirect('cart:detail')
