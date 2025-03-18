from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.

def home(request):
    return HttpResponse("Welcome")



def room_browsing(request):
    buildings = Building.objects.all()
    available_rooms = Room.objects.filter(is_available=True)

    return render(request, 'room_browsing.html', {'buildings': buildings, 'rooms': available_rooms})