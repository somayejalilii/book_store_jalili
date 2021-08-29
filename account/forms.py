from django import forms
from .models import BaseUser, Profile


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password_1 = forms.CharField(max_length=50,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد خود را وارد کنید'}))
    password_2 = forms.CharField(max_length=50,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد را مجدد وارد کنید'}))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if BaseUser.objects.filter(username=user).exists():
            raise forms.ValidationError('کاربر از قبل ایجاد شده است ')
        return user

    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('رمز را درست وارد کنید ')
        elif len(password2) < 5:
            raise forms.ValidationError('رمز عبور شما کمتر از پنج حرف است')
        return password1


class UserLoginForm(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=16,
                               widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد خود را وارد کنید'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['first_name','last_name','email']

class PhoneForms(forms.Form):
    phone = forms.IntegerField()

class CodeForm(forms.Form):
    code = forms.IntegerField()