from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'views', 'likes']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'tech_used']
    readonly_fields = ['created_at', 'views', 'likes']