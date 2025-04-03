from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from .models import MaintenanceRequest
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful registration
    else:
        form = RegisterForm()
    return render(request, 'dorm/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'dorm/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def maintenance_request_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        room_number = request.POST.get('room_number')
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        MaintenanceRequest.objects.create(
            name=name,
            room_number=room_number,
            issue_type=issue_type,
            description=description
        )

        return redirect('maintenance_success')  # Redirect to a success page

    return render(request, 'dorm/maintenance_req.html')

def maintenance_success_view(request):
    return render(request, 'dorm/maintenance_success.html')
