from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Welcome")

def start(request):
    return render(request, 'application/start.html')

def pg1(request):
    return render(request, 'application/page1.html', {'title': 'Page1'})

def pg2(request):
    building = None
    if request.method == 'POST':
        building = request.POST.get('building')
    return render(request, 'application/page2.html', {'title': 'Page2', 'building': building})

def confirmation(request):
    return render(request, 'application/confirmation.html', {'title': 'Submitted!'})


def room_browsing(request):
    buildings = Building.objects.all()
    available_rooms = Room.objects.filter(is_available=True)

    return render(request, 'room_browsing.html', {'buildings': buildings, 'rooms': available_rooms})

@login_required
def home(request):
 return render(request, "home.html", {})


def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})