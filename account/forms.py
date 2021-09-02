from django import forms
from .models import BaseUser, Profile


class UserRegisterForm(forms.Form):
    """
    ایجاد فرم برای ثبت نام کاربر
    """
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password_1 = forms.CharField(max_length=50,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد خود را وارد کنید'}))
    password_2 = forms.CharField(max_length=50,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد را مجدد وارد کنید'}))

    def clean_user_name(self):
        """
        در این متد بررسی میشود که کاربر قبلا ثبت نام نکرده باشد
        :return:

        """
        user = self.cleaned_data['user_name']
        if BaseUser.objects.filter(username=user).exists():
            raise forms.ValidationError('کاربر از قبل ایجاد شده است ')
        return user

    def clean_password_2(self):
        """
        جهت ارسال مجدد پسوورد و بررسی مساوی بودن پسوورد و تکرار پسووردو
         همچنین اضافه کردن شرط پسوورد باید بیشتر از پنج حرف باشد
        :return:
        """
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('رمز را درست وارد کنید ')
        elif len(password2) < 5:
            raise forms.ValidationError('رمز عبور شما کمتر از پنج حرف است')
        return password1


class UserLoginForm(forms.Form):
    """
    ایجاد فرم لاگین
    """
    user_name = forms.CharField(max_length=50)
    # email = forms.EmailField()
    password = forms.CharField(max_length=16,
                               widget=forms.PasswordInput(attrs={'placeholder': 'پسوورد خود را وارد کنید'})
                               )


class UserUpdateForm(forms.ModelForm):
    """
    ایجاد فرم جهت آپدیت پروفایل با استفاده از کلاس متا و استفاده از فیلد های کلاس یوزر
    """
    class Meta:
        model = BaseUser
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    ایجاد فرم جهت آپدیت پروفایل با استفاده از کلاس متا و استفاده از فیلد های کلاس پروفایل
    """
    class Meta:
        model = Profile
        fields = ['phone','address','profile_image']

class PhoneForms(forms.Form):
    phone = forms.IntegerField()

class CodeForm(forms.Form):
    code = forms.IntegerField()