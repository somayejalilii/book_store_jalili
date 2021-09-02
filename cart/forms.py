from django import forms


class CartAddForm(forms.Form):
    """
     فرم اضافه کردن تعداد  محصول برای سفارش و ثبت در سبد خریدایجاد
    """
    quantity = forms.IntegerField(max_value=9, min_value=1)


class CartAddBooksForm:
    pass
