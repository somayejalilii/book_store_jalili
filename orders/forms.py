from django import forms

class CouponForm(forms.Form):
    """
    فرم کد تخفیف
    """
    code = forms.CharField(max_length=100)
