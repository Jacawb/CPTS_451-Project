from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
  

    def __str__(self):
        return self.username

class MaintenanceRequest(models.Model):
    name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    issue_type = models.CharField(
        max_length=50,
        choices=[
            ('Plumbing', 'Plumbing'),
            ('Electrical', 'Electrical'),
            ('Heating/Cooling', 'Heating/Cooling'),
            ('Furniture', 'Furniture'),
            ('Other', 'Other'),
        ]
    )
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.issue_type} ({self.room_number})"
