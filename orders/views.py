from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart
from .forms import CouponForm
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
from django.utils.crypto import get_random_string


# Create your views here.
def home_page(request):
    return render(request, 'base.html')


def order_detail(request, id):
    """
    ثبت سفارش
    :param request:
    :param id:
    :return:
    """
    order = Ordering.objects.get(id=id)
    form = CouponForm()
    context = {
        'order': order,
        'form': form
    }
    return render(request, 'orders.html', context)


def order_create(request):
    """
    ایجاد سفارش و ارسال به صفحه جدید جهت پرداخت
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Ordering.objects.create(first_name=['first_name'],
                                            last_name=['last_name'], code=code)
            cart = Cart.objects.filter(user_id=request.user.id)
            for cart in cart:
                ShoppingCart.objects.create(order_id=order.id, user_id=request.user.id, book_id=cart.product_id)
            Cart.objects.filter(user_id=request.user.id).delete()
            messages.success(request, 'سفارش شما ایجاد شد')
            return redirect('orders:order_detail', order.id)


@require_POST
def coupon_order(request,id):
    """
    اعمال کد تخفیف و بررسی درست یا غلط بودن کد وارد شده
    """
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

# def send_request(request,id):
#     return redirect('account:history')


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify/'


def send_request(request,price,id):
    """
    ایجاد درگاه بانکی
    :param request:
    :param price:
    :param id:
    :return:
    """
    global amount
    amount = price
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": request.user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        order = Ordering.objects.get(id=id)
        order.paid = True
        order.save()
        cart = ShoppingCart.objects.filter(order_id=id)
        for c in cart:
            product = Book.objects.get(id=c.book.id)
            product.amount = c.number
            product.save()
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    """
    پرداخت
    :param request:
    :return:
    """
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')