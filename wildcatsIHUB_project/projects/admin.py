from django.contrib import admin
from .models import Project, Category  # Import Category

# --- Register Category Model ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
# -------------------------------

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'views', 'likes']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'tech_used']
    readonly_fields = ['created_at', 'views', 'likes']