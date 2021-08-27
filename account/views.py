from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import BaseUser, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = BaseUser.objects.create_user(username=data['user_name'], first_name=data['first_name'],
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


def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'profile.html', {'profile': profile})


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل بروزرسانی شد', 'success')
            return redirect('account:profile')
    else:
        user_form = UserUpdateForm(instance=request.user.profile)
        profile_form = ProfileUpdateForm()
    return render(request, 'update.html', {'user_form': user_form, 'profile_form': profile_form})
