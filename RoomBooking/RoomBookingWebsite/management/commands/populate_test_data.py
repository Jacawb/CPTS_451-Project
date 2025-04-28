from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from RoomBookingWebsite.models import (
    Student, Furnishing, Room, Building, Application, RoomAssignment
)
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Populate test data for buildings, rooms, applications, and assignments"

    def handle(self, *args, **kwargs):
        
        # Clear many-to-many relationships first
        for room in Room.objects.all():
            room.furnishings.clear()

        # Delete records
        Application.objects.all().delete()
        RoomAssignment.objects.all().delete()
        Room.objects.all().delete()
        Building.objects.all().delete()
        Furnishing.objects.all().delete()

        # Recheck deletion
        if Room.objects.filter(room_number="101A").exists():
            self.stdout.write(self.style.ERROR("Failed to clear data."))
            return

        # Create Furnishings
        bed1 = Furnishing.objects.create(type="Bed", is_available=True)
        bed2 = Furnishing.objects.create(type="Bed", is_available=True)
        desk = Furnishing.objects.create(type="Desk", is_available=True)
        closet = Furnishing.objects.create(type="Closet", is_available=True)

        # Create Buildings
        building1 = Building.objects.create(name="Dormitory A", floors=12)
        building2 = Building.objects.create(name="Dormitory B", floors=13)

        # Create Rooms
        room1 = Room.objects.create(
            room_number="101A",
            floor_number=1,
            building_id=building1.id,
            size_sqft=200,
            total_occupancy=2,
            is_available=True
        )

        room2 = Room.objects.create(
            room_number="102B",
            floor_number=1,
            building_id=building2.id,
            size_sqft=250,
            total_occupancy=3,
            is_available=True
        )

        # Add Furnishings to Rooms
        room1.furnishings.add(bed1, desk)
        room2.furnishings.add(bed2, closet)

        # Create Applications
        Application.objects.create(
            student=student,
            room=room1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            status='Pending'
        )

        Application.objects.create(
            student=student,
            room=room2,
            start_date=date.today(),
            end_date=None,
            status='Approved'
        )

        # Create Room Assignment
        RoomAssignment.objects.create(
            student=student,
            room=room2,
            start_date=date.today(),
            end_date=None
        )

        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
