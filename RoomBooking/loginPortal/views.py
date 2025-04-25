# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm
from RoomBookingWebsite.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import json

# @login_required
def home(request):
 return render(request, "loginPortal/home.html", {})

def RegistrationPage(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        form.fields.pop('roommates', None)
        if form.is_valid():
            # Build user
            user = form.save()
            user.email=form.cleaned_data['email']
            user.first_name=form.cleaned_data['first_name']
            user.last_name=form.cleaned_data['last_name']

            # Build student specific attributes
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_numbers = form.cleaned_data['phone_numbers']

            # Build student
            student = Student.objects.create(
                user=user,
                gender=gender,
                age=age,
                date_of_birth=date_of_birth,
                phone_numbers=[phone_numbers],

            )

            student.save()

            return redirect('/application')
    else:
        form = StudentRegistrationForm()
        form.fields.pop('roommates', None)
    return render(request, "loginPortal/registration/signup.html", {"form": form})

def LoginPage(request):
    print("Login view triggered")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/application/userinfo')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPortal/registration/login.html', {'form': form})
