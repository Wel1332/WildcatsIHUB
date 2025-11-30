from django import forms
from django.contrib.auth.models import User
from accounts.models import UserProfile 
from projects.models import Project

class ProjectForm(forms.ModelForm):
    """Form for editing all fields of the Project model."""
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'category', 'tech_used', 'screenshot', 
            'github_url', 'live_demo', 'video_demo', 'status', 'likes', 'views'
        ]
        # Basic styling for project fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'tech_used': forms.TextInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }

class UserProfileEditForm(forms.ModelForm):
    """Form for editing related UserProfile data."""
    class Meta:
        model = UserProfile
        fields = ['department', 'year_level', 'student_id']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-input'}),
            
            # FIX: Change to a Dropdown (Select) with specific choices
            'year_level': forms.Select(
                choices=[
                    ('', 'Select Year Level'), # Default empty option
                    (1, '1st Year'),
                    (2, '2nd Year'),
                    (3, '3rd Year'),
                    (4, '4th Year'),
                    (5, '5th Year'),
                ],
                attrs={'class': 'form-input'}
            ),
            
            'student_id': forms.TextInput(attrs={'class': 'form-input'}),
        }

class UserManagementForm(forms.ModelForm):
    """Form for editing basic Django User attributes via Admin Panel."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            # Checkboxes usually use default browser styling or specific toggle classes
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }
        
class AdminProfileForm(forms.ModelForm):
    """Form to edit the related UserProfile model fields."""
    class Meta:
        model = UserProfile
        fields = ['avatar']