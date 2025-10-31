from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'department', 'year_level']
    list_filter = ['department', 'year_level']
    search_fields = ['user__username', 'student_id', 'user__email']