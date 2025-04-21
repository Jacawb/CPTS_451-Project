from django.shortcuts import render, redirect, get_object_or_404
from RoomBookingWebsite.models import Room, Student, RoomAssignment, Application


# This view is for managing rooms and their occupancy
def manage_rooms(request):
    rooms = Room.objects.all()
    assignments = RoomAssignment.objects.select_related('student', 'room')
   
    room_occupancy = {room.room_id: [] for room in rooms}
    for assignment in assignments:
        room_occupancy[assignment.room.room_id].append(assignment.student)

    context = {
        'rooms': rooms,
        'room_occupancy': room_occupancy,
    }
    return render(request, "adminPortal/manage_rooms.html", context)

# This view is for managing bookings and applications
def manage_bookings(request):
    applications = Application.objects.all()
    context = {
        'applications': applications,
    }
    return render(request, "adminPortal/manage_bookings.html", context)

# This view is for approving applications
def approve_application(request, application_id):
    application = Application.objects.get(id=application_id)
    room = application.room
    student = application.student

    # create the room assignment
    RoomAssignment.objects.create(
        student=student,
        room=room,
        start_date=application.start_date,
        end_date=application.end_date
    )

    # update the application status
    application.status = 'Approved'
    application.save()

    return redirect('adminPortal:manage_bookings')

# This view is for canceling applications
def cancel_application(request, application_id):
    application = Application.objects.get(id=application_id)
    application.status = 'Rejected'
    application.save()

    return redirect('adminPortal:manage_bookings')

# This view is for reassigning rooms
def reassign_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    current_assignment = RoomAssignment.objects.filter(room=room).first()

    if current_assignment:
        student = current_assignment.student
    else:
        student = None

    if request.method == 'POST':
        new_room_id = request.POST.get('new_room_id')
        new_room = get_object_or_404(Room, id=new_room_id)

        if new_room == room:
            return redirect('adminPortal:manage_rooms')
        
        RoomAssignment.objects.create(
            student=student,
            room=new_room,
            start_date=current_assignment.start_date,
            end_date=current_assignment.end_date
        )

        current_assignment.delete()

        return redirect('adminPortal:manage_rooms')
    

    return render(request, "adminPortal/reassign_room.html", {
        'room': room,
        'student': student,
    })

       

