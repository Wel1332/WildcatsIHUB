from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    DEPARTMENTS = [
        ('Computer Science', 'Computer Science'),
        ('Information Technology', 'Information Technology'),
    ]
    
    YEAR_LEVELS = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'), 
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    avatar = models.ImageField(
        upload_to='avatars/', 
        default='avatars/default_profile.png',
        blank=True,
        null=True
    )

    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    year_level = models.CharField(max_length=20, choices=YEAR_LEVELS)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"