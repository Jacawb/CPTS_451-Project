# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
# from .models import MaintenanceRequest
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# @login_required
def home(request):
 return render(request, "loginPortal/home.html", {})

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("login")
 else:
  form = UserCreationForm()
 return render(request, "loginPortal/registration/signup.html", {"form": form})

def LoginPage(request):
    print("Login view triggered")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPortal/registration/login.html', {'form': form})
