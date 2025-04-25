import csv
from datetime import datetime
from ast import literal_eval
from django.core.management.base import BaseCommand
from RoomBookingWebsite.models import *
from django.contrib.auth.models import User

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
        with open('RoomBookingWebsite/test_data/furnishing.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Furnishing.objects.create(
                    type=row['type'],
                    is_available=row['is_available'] == 'TRUE'
                )

        # Load Building Data
        with open('RoomBookingWebsite/test_data/building.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Building.objects.create(
                    name=row['building_name'],
                    floors=row['floors']
                )
        
        # Load Student Data
        with open('RoomBookingWebsite/test_data/student.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    phone_numbers = literal_eval(row['phone_numbers'])
                except (ValueError, SyntaxError):
                    phone_numbers = [row['phone_numbers'].strip("'\"")]
                
                user, created = User.objects.get_or_create(
                    username=row['email'],
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                    }
                )

                preferences_data = {
                    'smoking': row['smoking'] == 'TRUE',
                    'drinking': row['drinking'] == 'TRUE',
                    'tidy': row['tidy'] == 'TRUE',
                    'sleeping': row['sleeping'] == 'TRUE'
                }
                
                preferences = None
                if any(preferences_data.values()):
                    preferences = Preferences.objects.create(**preferences_data)

                Student.objects.create(
                    user=user,
                    preferences=preferences,
                    student_id=row['student_id'],
                    gender=row['gender'],
                    age=int(row['age']),
                    date_of_birth=row['DOB'],
                    phone_numbers=phone_numbers,
                )

        # Load Room Data
        with open('RoomBookingWebsite/test_data/room.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                building_id = str(row['building_id'])[:10]
                Room.objects.create(
                    room_number=row['room_number'],
                    floor_number=int(row['floor_number']),
                    building_id=building_id,
                    size_sqft=int(row['size_sqft']),
                    total_occupancy=int(row['total_occupancy']),
                    is_available=row['is_available'] == 'TRUE',
                )
        
        # Load Maintenance Worker Data
        with open('RoomBookingWebsite/test_data/maintenance_worker.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                MaintenanceWorker.objects.create(
                    maintenance_id=row['maintenance_id'],
                    first_name=row['first_name_m'],
                    last_name=row['last_name_m']
                )

        # Load Administrator Data
        with open('RoomBookingWebsite/test_data/administrator.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user, created = User.objects.get_or_create(
                    username=row['email_a'],
                    defaults={
                        'email': row['email_a'],
                        'first_name': row['first_name_a'],
                        'last_name': row['last_name_a'],
                    }
                )

                Administrator.objects.create(
                    user=user,
                    admin_id=row['admin_id'],
                )

        # Load Maintenance Request Data
        with open('RoomBookingWebsite/test_data/maintenance_request.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                request_date = datetime.strptime(row['request_date'], '%Y-%m-%d').date()
                MaintenanceRequest.objects.create(
                    name=row['name'],
                    room_number=row['room_number'],
                    issue_type=row['issue_type'],
                    description=row['description'],
                    submitted_at=request_date,
                )

        # Load Application Data
        with open('RoomBookingWebsite/test_data/applications.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    student = Student.objects.get(student_id=row['student_id'])
                    room = Room.objects.get(room_number=row['room_number'])
                    Application.objects.create(
                        student=student,
                        room=room,
                        start_date=row['start_date'],
                        end_date=row['end_date'] if row['end_date'] else None,
                        status=row['status']
                    )
                except Student.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Student {row['student_id']} not found for application."
                    ))
                except Room.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Room {row['room_number']} not found for application."
                    ))

        # Load room_assignment Data
        with open('RoomBookingWebsite/test_data/room_assignment.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    student = Student.objects.get(student_id=row['student_id'])
                    room = Room.objects.get(room_number=row['room_number'])
                    RoomAssignment.objects.create(
                        student=student,
                        room=room,
                        start_date=row['start_date'],
                        end_date=row['end_date'] if row['end_date'] else None
                    )
                except Student.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Student {row['student_id']} not found for room assignment."
                    ))
                except Room.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Room {row['room_number']} not found for room assignment."
                    ))


        
        self.stdout.write(self.style.SUCCESS("Test data populated successfully!"))
