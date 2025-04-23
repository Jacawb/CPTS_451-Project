# https://www.youtube.com/watch?v=6aQoW0TRXBk

from django.forms import ModelForm
from django import forms
from RoomBookingWebsite.models import *

class Pg1Form(ModelForm):
    User.first_name = forms.TextInput()
    phone_numbers = forms.NumberInput()
    class Meta:
        model = Student
        fields = ['student_id','phone_numbers']

class RoomForm(ModelForm):
    # student = 
    room = forms.ChoiceField()
    # start_date = models.DateField()
    # end_date = models.DateField(null=True, blank=True)
    # status = models.CharField(max_length=20, choices=[
    #     ('Pending', 'Pending'),
    #     ('Approved', 'Approved'),
    #     ('Rejected', 'Rejected'),
    # ])