from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
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
    
class Room(models.Model):

    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10, unique=True)
    floor_number = models.IntegerField()
    building_id = models.CharField(max_length=10)
    size_sqft = models.IntegerField()
    total_occupancy = models.IntegerField()
    furnishings = models.ManyToManyField(Furnishing, blank=True)
    is_available = models.BooleanField(default=True)

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue = models.TextField()
    maintenance_worker = models.ForeignKey(
        MaintenanceWorker, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class FurnishingRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    furnishing = models.ForeignKey(Furnishing, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Building(models.Model):
    name = models.CharField(max_length=100)

