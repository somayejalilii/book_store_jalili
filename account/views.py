from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, PhoneForms, CodeForm
from .models import BaseUser, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
# from restapi import restfulapi


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = BaseUser.objects.create_user(username=data['user_name'], email='email',
                                                first_name=data['first_name'],
                                                last_name=data['last_name'], password=data['password_1'])
            messages.success(request, 'ثبت نام موفقیت آمیز بود', 'success')
            user.save()
            return redirect('book:list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, user_name=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'به وب سایت فروشگاه کتاب خوش آمدید', 'primary')
                return redirect('book:list')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید', 'info')
    return redirect('book:list')


@login_required(login_url='account:login')
def user_profile(request):
    profile = BaseUser.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='account:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.first_name)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل بروزرسانی شد', 'success')
            return redirect('account:profile')
    else:
        user_form = UserUpdateForm(instance=request.user.first_name)
        profile_form = ProfileUpdateForm()
    return render(request, 'update.html', {'user_form': user_form, 'profile_form': profile_form})


def change_password(request):
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
