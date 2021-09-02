from django import forms

class SearchForm(forms.Form):
    """ایجاد فرم سرچ بار"""
    search = forms.CharField()