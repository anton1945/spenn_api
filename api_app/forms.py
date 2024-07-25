from django import forms
from .models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['phone_number', 'amount', 'message']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-sm form-control-custom-width'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm form-control-custom-width'}),
            'message': forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-custom-width'}),
        }

class CheckStatusForm(forms.Form):
    request_id = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))