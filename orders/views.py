from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages


# Create your views here.
def home_page(request):
    return render(request, 'base.html')


def order_detail(request, id):
    order = Ordering.objects.get(id=id)
    form = CouponForm()
    context = {'order': order, 'form': form}
    return render(request, 'orders.html', context)


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


@require_POST
def coupon_order(request, id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'کد وارد شده درست نمیباشد', 'danger')
            return redirect('orders:order_detail', id)
        order = Ordering.objects.get(id=id)
        order.discount = coupon.discount
        order.save()
    return redirect('orders:order_detail', id)
