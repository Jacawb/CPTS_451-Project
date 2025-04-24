from django.shortcuts import render, redirect
from applicationPortal.forms import *
from RoomBookingWebsite.models import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def start(request):
    return render(request, 'applicationPortal/start.html')

def pg1(request):
    # Prereq: manage.py populate_test_data
    try:
        student = Student.objects.select_related('user').get(user__email='john.doe@example.com')
    except Student.DoesNotExist:
        return render(request, 'applicationPortal/page1.html', {
            'error': 'Test student not found. Please run "manage.py populate_test_data".'
        })
    
    user=student.user

    if not request.user.is_authenticated:
        login(request, user)

    if request.method == 'POST':
        phone_input = request.POST.get('phone_numbers', '')
        phone_numbers = [num.strip() for num in phone_input.strip().splitlines() if num.strip()]

        move_in_date = request.POST.get('move_in_date')

        student.phone_numbers = phone_numbers
        # student.move_in_date = move_in_date
        student.save()

        # Redirect or render success message
        return redirect('pg1')  # Reloads the page or change to a success URL

    # If GET, display form with current data
    context = {
        'current_name': f"{student.user.first_name} {student.user.last_name}",
        'form': {
            'phone_numbers': '\n'.join(student.phone_numbers or [])
        },
        'title': 'Page1'
    }

    return render(request, 'applicationPortal/page1.html', context)



def pg2(request):
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

    return render(request, 'applicationPortal/page2.html', {
        'buildings': buildings,
        'rooms': available_rooms,
        'title': 'Page2',
        'selected_building_id': selected_building_id  # Pass the selected building ID to the template
    })
    # return render(request, ', {'title': 'Page2', 'building': building})

def pg3(request):
    if request.method == 'POST':
        student = request.user.student_profile

        # check if the student has preferences
        if not student.preferences:
            prefs = Preferences.objects.create()
            student.preferences = prefs
            student.save()
        else:
            prefs = student.preferences
 
        prefs.drinking = request.POST.get('drink') == 'yes'
        prefs.smoking = request.POST.get('smoke') == 'yes'
        prefs.tidy = request.POST.get('cleanliness') == 'tidy'
        prefs.sleeping = request.POST.get('bedtime') == 'early'
        prefs.save()

        return redirect('/application/confirm/')

    return render(request, 'applicationPortal/page3.html', {'title': 'Page3'})

def confirmation(request):
    return render(request, 'applicationPortal/confirmation.html', {'title': 'Submitted!'})

@login_required
def userinfo(request):
    student = request.user.student_profile
    
    applications = Application.objects.filter(student=student)
    roomAssignment = RoomAssignment.objects.filter(student=student)
    return render (request, 'applicationPortal/viewuserinfo.html', {
        'student':student,
        'applications':applications,
        'assignment':roomAssignment,
    })
