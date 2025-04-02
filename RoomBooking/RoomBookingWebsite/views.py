from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def home(request):
    return HttpResponse("Welcome")

def room_browsing(request):
    buildings = Building.objects.all()
    selected_building_id = request.GET.get('building_id', '')

    # Filter rooms based on selected building
    if selected_building_id:
        available_rooms = Room.objects.filter(building_id=selected_building_id, is_available=True)
    else:
        available_rooms = Room.objects.filter(is_available=True)

    return render(request, 'RoomBookingWebsite/RoomBrowsing.html', {'buildings': buildings, 'rooms': available_rooms})
