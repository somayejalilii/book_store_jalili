from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

from book.models import Book
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, PhoneForms, CodeForm
from .models import BaseUser, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
from django.core.mail import EmailMessage
# from restapi import restfulapi
from django.views import View
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from orders.models import ShoppingCart


class EmailToken(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))


email_generator = EmailToken()


def user_register(request):
    """
    ثبت نام کاربر و بررسی ورود اطلاعات درست
     فعال کردن کاربر با ارسال ایمیل
      هش پسوورد
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = BaseUser(username=data['user_name'], email=data['email'],
                            first_name=data['first_name'],
                            last_name=data['last_name'])
            user.set_password(data['password_1'])
            messages.success(request, 'ثبت نام موفقیت آمیز بود', 'success')
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes((user.id)))
            url = reverse('account:active', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'active user',
                link,
                'test<s68jalili@gmail.com>',
                [data['email']],
            )
            email.send(fail_silently=False)
            messages.warning(request, 'کاربر محترم لطفا برای فعالسازی به ایمیل خود مراجعه کنید', 'warning')
            return redirect('book:list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class RegisterEmail(View):

    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = BaseUser.objects.get(id=id)
        if user and email_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('account:login')


def user_login(request):
    """
    بررسی نام کاربری و پسوورد جهت ورود کاربر
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # user = authenticate(username=data['user_name'], password=data['password'])
            try:
                user = BaseUser.objects.get(username=data['user_name'])
                if user.check_password(data['password']):
                    login(request, user)
                    messages.success(request, 'به وب سایت فروشگاه کتاب خوش آمدید', 'primary')
                    return redirect('book:list')

                else:
                    messages.success(request, 'رمز یا نام کاربری اشتباه است', 'primary')
            except BaseUser.DoesNotExist:
                messages.success(request, 'نام کاربری یا رمز عبور اشتباه است !!!', 'primary')

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    """
    خروج کاربر
    :param request:
    :return:
    """
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'info')
    return redirect('book:list')


@login_required(login_url='account:login')
def user_profile(request):
    """
    صفحه پروفایل کاربر
    :param request:
    :return:
    """
    # profile = Profile.objects.get(user_id=request.user.profile)
    return render(request, 'profile.html', {'profile': request.user})


@login_required(login_url='account:login')
def user_update(request):
    """
    بروزرسانی و تغییر اطلاعات توسط کاربر
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل بروزرسانی شد', 'success')
            return redirect('account:profile')
    else:
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()
    return render(request, 'update.html', {'user_form': user_form, 'profile_form': profile_form})


def change_password(request):
    """
    تغییر پسوورد با ارسال ایمیل به کاربر
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'پسوورد با موفقیت تغییر کرد')
            return redirect('account:profile')
        else:
            messages.success(request, 'پسوورد درست انتخاب نشده است', 'danger')
            return redirect('account:change_password')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change.html', {'form': form})


def favorite(request,id):
    """
    ایجاد صفحه علاقه مندی های کاربر
    :param request:
    :param id:
    :return:
    """
    book = request.user.fa_user.all()
    return render(request, 'favorite.html', {'book': book})


def history(request):
    """
    ایجاد تاریخچه خرید و نمایش اطلاعات ثبت و خرید کاربر
    :param request:
    :return:
    """
    data = ShoppingCart.objects.filter(user=request.user)
    return render(request, 'history.html', {'data': data})


class ResetPassword(auth_views.PasswordResetView):
    """
    تغییر پسوورد
    """
    template_name = 'reset.html'
    success_url = reverse_lazy('account:reset_done')
    email_template_name = 'link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'done.html'


class password_reset_confirm(auth_views.PasswordResetConfirmView):
    template_name = 'confirm.html'
    success_url = reverse_lazy('account:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'complete.html'

# def phone(request):
#     if request.method == 'POST':
#         form = PhoneForms(request.POST)
#         if form.is_valid():
#             global random_code, phone
#             data = form.cleaned_data
#             phone = f"0{data['phone']}"
#             random_code = randint(100, 1000)
#             ws = restfulapi("*****", "*****")
#             ws.SendMessage(PhoneNumber=phone, Message=random_code, Mobiles=['9193073314'],
#                            SendDateInTimeStamp=1558298601)
#             return redirect('account:verify')
#     else:
#         form = PhoneForms()
#     return render(request, 'phone.html', {'form': form})
#
#
# def verify(request):
#     if request.method == 'POST':
#         form = CodeForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             if random_code == data['code']:
#                 profile = Profile.objects.get(phone=phone)
#                 user = BaseUser.objects.get(profile__id=profile.user.id)
#                 login(request, user)
#                 messages.success(request,'خوش آمدید')
#                 return redirect('book:list')
#             else:
#                 messages.success(request, 'کد شما اشتباه است')
#     else:
#         form = CodeForm()
#     return render(request, 'code.html', {'form': form})
