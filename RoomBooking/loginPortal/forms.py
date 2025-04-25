from django import forms
from django.contrib.auth.forms import UserCreationForm
from RoomBookingWebsite.models import *

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = forms.IntegerField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_numbers = forms.CharField(
        required=True,
        help_text="Enter phone numbers separated by commas (e.g., 1234567890,0987654321)"
    )
    roommates = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2'
        ]
