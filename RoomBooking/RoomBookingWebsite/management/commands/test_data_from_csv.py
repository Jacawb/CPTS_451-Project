import csv
from django.core.management.base import BaseCommand
from RoomBookingWebsite.models import *

class Command(BaseCommand):
    help = 'Load test data from CSV files into the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Room.objects.all().delete()
        Building.objects.all().delete()
        Furnishing.objects.all().delete()
        Student.objects.all().delete()
        MaintenanceWorker.objects.all().delete()
        Administrator.objects.all().delete()
        MaintenanceRequest.objects.all().delete()

        # Load Furnishing Data
        with open('RoomBooking/RoomBookingWebsite/test_data/furnishing.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Furnishing.objects.create(
                    type=row['type'],
                    is_available=row['is_available'] == 'TRUE'
                )

        # Load Building Data
        with open('RoomBooking/RoomBookingWebsite/test_data/building.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Building.objects.create(
                    name=row['building_name'],
                    floors=row['floors']
                )
        
        # Load Student Data
        with open('RoomBooking/RoomBookingWebsite/test_data/student.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Student.objects.create(
                    student_id=row['student_id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    phone_number=row['phone'],
                    DOB=row['DOB'],
                    Gender=row['Gender']
                )

        # Load Room Data
        with open('RoomBooking/RoomBookingWebsite/test_data/room.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                room = Room.objects.create(
                    room_number=row['room_number'],
                    floor_number=row['floor_number'],
                    building=Building.objects.get(name=row['building_name']),
                    size_sqft=row['size_sqft'],
                    total_occupancy=row['total_occupancy'],
                    is_available=row['is_available'] == 'TRUE',
                    residents=row['residents'] or ""
                )
        
        # Load Maintenance Worker Data
        with open('RoomBooking/RoomBookingWebsite/test_data/maintenance_worker.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                MaintenanceWorker.objects.create(
                    maintenance_id=row['maintenance_id'],
                    first_name=row['first_name_m'],
                    last_name=row['last_name_m'],
                    email=row['email_m'],
                    phone_number=row['phone_number_m']
                )

        # Load Administrator Data
        with open('RoomBooking/RoomBookingWebsite/test_data/administrator.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Administrator.objects.create(
                    admin_id=row['admin_id'],
                    first_name=row['first_name_a'],
                    last_name=row['last_name_a'],
                    email=row['email_a'],
                    phone_number=row['phone_number_a']
                )

        # Load Maintenance Request Data
        with open('RoomBooking/RoomBookingWebsite/test_data/maintenance_request.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                MaintenanceRequest.objects.create(
                    request_id=row['request_id'],
                    room=Room.objects.get(room_number=row['room_number']),
                    issue=row['issue'],
                    request_date=row['request_date'],
                )
        
        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
