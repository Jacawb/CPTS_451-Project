from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def home(request):
    return HttpResponse("Welcome")

def room_browsing(request):
    populate_test_data()
    buildings = Building.objects.all()
    available_rooms = Room.objects.filter(is_available=True)

    return render(request, 'RoomBookingWebsite/RoomBrowsing.html', {'buildings': buildings, 'rooms': available_rooms})

def populate_test_data():
    if Room.objects.filter(room_number="101A").exists():
        return
     
    # Create Furnishings
    bed = Furnishing.objects.create(type="Bed", is_available=True)
    desk = Furnishing.objects.create(type="Desk", is_available=True)
    closet = Furnishing.objects.create(type="Closet", is_available=True)
    
    # Create Buildings
    building1 = Building.objects.create(name="Dormitory A")
    building2 = Building.objects.create(name="Dormitory B")
    
    # Create Rooms
    room1 = Room.objects.create(
        room_number="101A",
        floor_number=1,
        building_id=building1.id,
        size_sqft=200,
        total_occupancy=2,
        is_available=True,
        residents=""
    )
    room2 = Room.objects.create(
        room_number="102B",
        floor_number=1,
        building_id=building2.id,
        size_sqft=250,
        total_occupancy=3,
        is_available=False,
        residents="John Doe, Jane Doe"
    )
    
    # Add Furnishings to Rooms
    room1.furnishings.add(bed, desk)
    room2.furnishings.add(bed, closet)
    
    return HttpResponse("Test data populated successfully!")