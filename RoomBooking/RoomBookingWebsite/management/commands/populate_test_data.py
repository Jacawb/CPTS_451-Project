from django.core.management.base import BaseCommand
from RoomBookingWebsite.models import *

class Command(BaseCommand):
    help = "Populate test data for buildings and rooms"

    def handle(self, *args, **kwargs):

        # Simulated logged-in or test user
        test_user, _ = User.objects.get_or_create(
            email='john.doe@example.com',
            defaults={
                'username': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )

        student, created = Student.objects.get_or_create(
        user=test_user,
        defaults={
            'age': 20,
            'gender': 'Male',
            'date_of_birth': '2004-01-15', 
            'phone_numbers': ['1234567890'],
        }
        )

        # Clear many-to-many relationships first
        for room in Room.objects.all():
            room.furnishings.clear()

        # Delete records
        Room.objects.all().delete()
        Building.objects.all().delete()
        Furnishing.objects.all().delete()

        if Room.objects.filter(room_number="101A").exists():
            self.stdout.write(self.style.SUCCESS("Failed to clear data."))
            return

        # Create Furnishings
        bed1 = Furnishing.objects.create(type="Bed", is_available=True)
        bed2 = Furnishing.objects.create(type="Bed", is_available=True)
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

        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))