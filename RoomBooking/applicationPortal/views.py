from django.shortcuts import render
from .models import *

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
