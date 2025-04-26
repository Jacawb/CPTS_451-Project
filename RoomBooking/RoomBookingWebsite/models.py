from django.db import models
from django.contrib.auth.models import User

class Preferences(models.Model):
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    tidy = models.BooleanField(default=False)
    sleeping = models.BooleanField(default=False)
    def match_score(self, other):
        score = 0
        if not other:
            return score
        score += self.smoking == other.smoking
        score += self.drinking == other.drinking
        score += self.tidy == other.tidy
        score += self.sleeping == other.sleeping
        return score

    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    preferences = models.OneToOneField(Preferences, on_delete=models.CASCADE, null=True, blank=True, related_name='student_preferences')
    
    student_id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = models.IntegerField()
    date_of_birth = models.DateField()
    phone_numbers = models.JSONField()  # List of phone numbers
    matched = models.BooleanField(default=False)

    def __str__(self):
        return f"Student {self.student_id} - {self.user.username}"

class StudentRoommates(models.Model):
    student1 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='roommate_set_1')
    student2 = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='roommate_set_2')
    assigned_on = models.DateTimeField(auto_now_add=True)
    roommates = models.ManyToManyField("self", symmetrical=True, blank=True)


    def __str__(self):
        return f"{self.student1.user.username} & {self.student2.user.username}"


class Furnishing(models.Model):
    furniture_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)  # e.g., "Bed", "Desk", "Closet"
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} (ID: {self.furniture_id})"

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
    
    def __str__(self):
        return f"{self.name}"

class Room(models.Model):

    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10, unique=True)
    floor_number = models.IntegerField()
    building_name=models.CharField(max_length=100, default='error')
    building_id = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="rooms")
    size_sqft = models.IntegerField()
    total_occupancy = models.IntegerField()
    furnishings = models.ManyToManyField(Furnishing, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - Floor {self.floor_number} in {self.building_name}"

class RoomAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Assignment: {self.student.user.username} to {self.room.room_number}"

class MaintenanceWorker(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Maintenance Worker"
    
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrator_profile')
    
    admin_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Administrator {self.user.username}"

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

    def __str__(self):
        return f"Request: {self.name} - {self.issue_type} in Room {self.room_number}"
    
class FurnishingRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    furnishing = models.ForeignKey(Furnishing, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Furnishing Request by {self.student.user.username} for {self.furnishing.type} in {self.room.room_number}"


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

    def __str__(self):
        return f"Application {self.student.user.username} for {self.room.room_number} - {self.status}"