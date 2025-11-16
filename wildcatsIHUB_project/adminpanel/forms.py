# adminpanel/forms.py

from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile 
from projects.models import Project

class ProjectForm(forms.ModelForm):
    """Form for editing all fields of the Project model."""
    class Meta:
        model = Project
        # List the fields an admin should be able to modify
        fields = [
            'title', 'description', 'category', 'tech_used', 'screenshot', 
            'github_url', 'live_demo', 'video_demo', 'status', 'likes', 'views'
        ]

class UserProfileEditForm(forms.ModelForm):
    """Form for editing related UserProfile data."""
    class Meta:
        model = UserProfile
        # Fields relevant for editing a student/user profile
        fields = ['department', 'year_level', 'student_id']

class UserManagementForm(forms.ModelForm):
    """Form for editing basic Django User attributes via Admin Panel."""
    class Meta:
        model = User
        # Fields an admin should manage for another user
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']


class AdminUserForm(forms.ModelForm):
    """Form to edit the basic User model fields (first_name, last_name, email)."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class AdminProfileForm(forms.ModelForm):
    """Form to edit the related UserProfile model fields (department, etc.)."""
    
    class Meta:
        model = UserProfile
        fields = ['avatar']