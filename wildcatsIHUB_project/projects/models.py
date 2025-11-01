from django.db import models
from accounts.models import UserProfile  # Import from accounts app

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_demo = models.URLField(blank=True, null=True)
    video_demo = models.URLField(blank=True, null=True)
    tech_used = models.CharField(max_length=200, blank=True, null=True)
    screenshot = models.ImageField(upload_to="project_screenshots/", blank=True, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True) 
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']  
    
    def __str__(self):
        return self.title