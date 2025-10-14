from django.db import models
from django.contrib.auth.models import User

# Custom User Profile table
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
    
    # Link to Django's built-in User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Additional fields you want to store
    student_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    year_level = models.CharField(max_length=20, choices=YEAR_LEVELS)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    video_demo = models.URLField(blank=True, null=True)
    tech_used = models.CharField(max_length=200, blank=True, null=True)
    screenshot = models.ImageField(upload_to="project_screenshots/", blank=True, null=True)
    
    # Link project to UserProfile
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title