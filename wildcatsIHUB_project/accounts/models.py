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
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    year_level = models.CharField(max_length=20, choices=YEAR_LEVELS)
    
    # Profile information fields
    full_name = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    school = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    graduation_yr = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    specialization = models.TextField(blank=True, null=True)
    major = models.TextField(blank=True, null=True)
    minor = models.TextField(blank=True, null=True)
    courses = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    
    avatar = models.ImageField(
        upload_to='avatars/', 
        default='avatars/default_profile.png',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"