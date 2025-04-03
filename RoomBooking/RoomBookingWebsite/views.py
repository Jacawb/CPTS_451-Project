from django.shortcuts import render, HttpResponse
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