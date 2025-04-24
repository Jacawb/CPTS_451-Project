from django import forms
from django.contrib.auth.forms import UserCreationForm
from RoomBookingWebsite.models import *

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)
   

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']