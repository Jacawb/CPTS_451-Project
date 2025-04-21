from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

def home(request):
    return HttpResponse("Welcome")

def room_browsing(request):
    buildings = Building.objects.all()
    selected_building_id = request.GET.get("building_id")

    if selected_building_id is None:
        selected_building_id = 0  # Default to "All Buildings"
    elif selected_building_id == "":
        selected_building_id = 0  # Ignore empty requests, treat as "All Buildings"
    else:
        try:
            selected_building_id = int(selected_building_id)  # Convert to int safely
        except ValueError:
            selected_building_id = 0  # Fallback in case of invalid input

    # Filter rooms based on selected building
    if selected_building_id > 0:
        available_rooms = Room.objects.filter(building_id=selected_building_id, is_available=True).prefetch_related('furnishings')
    else:
        available_rooms = Room.objects.filter(is_available=True).prefetch_related('furnishings')

    return render(request, 'RoomBookingWebsite/RoomBrowsing.html', {
        'buildings': buildings,
        'rooms': available_rooms,
        'selected_building_id': selected_building_id  # Pass the selected building ID to the template
    })

def start(request):
    return render(request, 'RoomBookingWebsite/start.html')

def pg1(request):
    return render(request, 'RoomBookingWebsite/page1.html', {'title': 'Page1'})

def pg2(request):
    building = None
    if request.method == 'POST':
        building = request.POST.get('building')
    return render(request, 'RoomBookingWebsite/page2.html', {'title': 'Page2', 'building': building})

def pg3(request):
    return render(request, 'RoomBookingWebsite/page3.html', {'title': 'Page3'})

def confirmation(request):
    return render(request, 'RoomBookingWebsite/confirmation.html', {'title': 'Submitted!'})


@login_required
def home(request):
 return render(request, "RoomBookingWebsite/home.html", {})


def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "RoomBookingWebsite/signup.html", {"form": form})

def admin_home(request):
    return render(request, "RoomBookingWebsite/adminHome.html") 