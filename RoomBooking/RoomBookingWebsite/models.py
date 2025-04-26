from django.db import models
from django.contrib.auth.models import User

class Preferences(models.Model):
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    tidy = models.BooleanField(default=False)
    sleeping = models.BooleanField(default=False)
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    preferences = models.OneToOneField(Preferences, on_delete=models.CASCADE, null=True, blank=True, related_name='student_preferences')
    
    student_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = models.IntegerField()
    date_of_birth = models.DateField()
    phone_numbers = models.JSONField()  # List of phone numbers
    roommates = models.ManyToManyField("self", blank=True)

class Furnishing(models.Model):
    furniture_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)  # e.g., "Bed", "Desk", "Closet"
    is_available = models.BooleanField(default=True)

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True, default='error')
    floors = models.IntegerField(default=-1)
    bathroom_type = models.CharField(
        max_length=50,
        default="-",
        choices=[
            ('Private', 'Private'), 
            ('Semi-Private', 'Semi-Private'),
            ('Community', 'Community')
        ] )
    gender=models.CharField(
        max_length=50,
        default="-",
        choices=[
            ('men', 'men'),
            ('women', 'women'),
            ('coed', 'coed')
        ])
class Room(models.Model):

    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10, unique=True)
    floor_number = models.IntegerField()
    building_name=models.CharField(max_length=100, unique=True, default='error')
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="rooms")
    size_sqft = models.IntegerField()
    total_occupancy = models.IntegerField()
    furnishings = models.ManyToManyField(Furnishing, blank=True)
    is_available = models.BooleanField(default=True)

class RoomAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class MaintenanceWorker(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator_profile')
    
    admin_id = models.AutoField(primary_key=True)

class MaintenanceRequest(models.Model):
    name = models.CharField(max_length=100, default='Anonymous')
    room_number = models.CharField(max_length=10, default='Unknown')
    issue_type = models.CharField(
        max_length=50,
        choices=[
            ('Plumbing', 'Plumbing'),
            ('Electrical', 'Electrical'),
            ('Heating/Cooling', 'Heating/Cooling'),
            ('Furniture', 'Furniture'),
            ('Other', 'Other'),
        ],
        default='Other'
    )
    description = models.TextField(default='none')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
class FurnishingRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    furnishing = models.ForeignKey(Furnishing, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ])