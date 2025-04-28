from django.shortcuts import render, redirect, get_object_or_404
from applicationPortal.forms import *
from RoomBookingWebsite.models import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required (login_url='/login/')
def start(request):
    return render(request, 'applicationPortal/start.html')

def pg1(request):
    user=request.user

    # Authenticate user
    if user.is_authenticated:
        try:
            student = user.student_profile  # Assuming OneToOneField or ForeignKey relationship
        except Student.DoesNotExist:
            return HttpResponse("No associated student found.")
    else:
        return HttpResponse("User is not authenticated.")

    

    if request.method == 'POST':
        phone_input = request.POST.get('phone_numbers', '')
        phone_numbers = [num.strip() for num in phone_input.strip().splitlines() if num.strip()]

        move_in_date = request.POST.get('move_in_date')

        student.phone_numbers = phone_numbers
        # student.move_in_date = move_in_date
        student.save()

        # Redirect or render success message
        return redirect('application-pg1')  # Reloads the page or change to a success URL

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
    occupancy_filter = request.GET.get("occupancy")
    floor_filter = request.GET.get("floor")
    order_by = request.GET.get("order_by")

    try:
        selected_building_id = int(selected_building_id or 0)
    except ValueError:
        selected_building_id = 0

    # Start with available rooms
    if selected_building_id > 0:
        available_rooms = Room.objects.filter(building_id=selected_building_id, is_available=True)
    else:
        available_rooms = Room.objects.filter(is_available=True)

    # Apply occupancy filter
    if occupancy_filter:
        try:
            available_rooms = available_rooms.filter(total_occupancy=int(occupancy_filter))
        except ValueError:
            pass  # Ignore invalid input

    # Apply floor filter
    if floor_filter:
        try:
            available_rooms = available_rooms.filter(floor_number=int(floor_filter))
        except ValueError:
            pass

    # Apply sorting
    if order_by in ['size_sqft', '-size_sqft', 'total_occupancy', '-total_occupancy']:
        available_rooms = available_rooms.order_by(order_by)

    # Dynamically get floors available for selected building
    floors = []
    if selected_building_id:
        try:
            building = Building.objects.get(id=selected_building_id)
            floors = list(range(1, building.floors + 1))  # floors = [1, 2, ..., N]
        except Building.DoesNotExist:
            pass

    occupancy_options = [2, 3, 4]

    available_rooms.prefetch_related('furnishings')
    
    if request.method == 'POST':
        selected_room_id = request.POST.get("selected_room_id")
        print("Selected Room ID:", selected_room_id)
        
        if not selected_room_id:
            return HttpResponse("Room ID is missing or invalid.", status=400)

        # Ensure the selected_room_id persists even after other POST requests
        if selected_room_id:
            request.session['selected_room_id'] = selected_room_id
            request.session.modified = True  # Force session to save
        else:
            selected_room_id = request.session.get('selected_room_id')
            
        print("Session data:", request.session.items())  # Debug session contents
        return redirect('/application/page3/')
        
    return render(request, 'applicationPortal/page2.html', {
        'buildings': buildings,
        'rooms': available_rooms,
        'floors': floors,
        'selected_building_id': selected_building_id,
        'title': 'Page2',
        'occupancy_options': occupancy_options,
    })

def pg3(request):
    
    room_id = request.session.get('selected_room_id')
    if not room_id:
        return HttpResponse("No room selected", status=400)

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
        
        try:
            room = Room.objects.get(room_id=room_id)
        except Room.DoesNotExist:
            return HttpResponse(f"Room with ID {room_id} does not exist", status=404)

        Application.objects.create(
            student=student,
            room=room,    
            start_date=datetime.now(),
            end_date= None,
            status='Pending'
        )

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

    return render(request, 'applicationPortal/maintenance_req.html')

def maintenance_success_view(request):
    return render(request, 'applicationPortal/maintenance_success.html')

def approve_application(request, application_id):
    try:
        # Get the application by its ID
        application = Application.objects.get(id=application_id)

        # Update the application status
        application.status = "Approved"
        application.save()

        # Redirect back to the application change form in the admin panel
        return HttpResponseRedirect(reverse('admin:RoomBookingWebsite_application_change', args=[application.id]))

    except Application.DoesNotExist:
        # Handle case where the application is not found
        return HttpResponseRedirect(reverse('admin:index'))  # Redirect to the admin index 
    

def furnishing_request_success(request):
    if request.method == 'POST':
        student = request.user.student_profile

        furnishing_id = request.POST.get('furnishing_id')
        furnishing = Furnishing.objects.get(furniture_id=furnishing_id)  

        target_room_id = request.POST.get('room_id')
        room = Room.objects.get(room_id=target_room_id)  # <-- same here

        FurnishingRequest.objects.create(
            student=student,
            furnishing=furnishing,
            room=room,
        )

        return render(request, 'applicationPortal/furnishing_success.html')

    return render(request, 'applicationPortal/furnishing_success.html')

def furnishing_request_display(request):
    furnishings = Furnishing.objects.filter(is_available=True)

    student = request.user.student_profile

    roomAssign = RoomAssignment.objects.filter(student=student).first()

    target_room_id = roomAssign.room.room_id

    return render(request, 'applicationPortal/furnishing_display.html', {
        'furnishings': furnishings,
        'room_id':target_room_id
    })
