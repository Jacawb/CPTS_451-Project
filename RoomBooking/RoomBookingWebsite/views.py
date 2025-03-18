from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def home(request):
    return HttpResponse("Welcome")



def room_browsing(request):
    buildings = Building.objects.all()
    selected_building = request.GET.get('building')
    
    rooms = Room.objects.filter(buildingid=selected_building) if selected_building else Room.objects.none()

    return render(request, 'room_browsing.html', {
        'buildings': buildings,
        'rooms': rooms,
        'selected_building': selected_building
    })