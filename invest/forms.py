from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Withdrawal


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=11)
    coupon = forms.CharField(max_length=8)
    referal = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'coupon', 'referal')


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ('ac_name', 'ac_num', 'bank', 'review')
