from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from accounts.models import UserProfile  # Add this import

def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/view_project.html', {'project': project})

def delete_project(request, project_id):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
  
    project = get_object_or_404(Project, id=project_id, author=user_profile)
    project_title = project.title
    project.delete()
    messages.success(request, f"Project '{project_title}' deleted successfully!")
    
    return redirect('/profile/') 
def home(request):
    projects = Project.objects.all().select_related('author__user')  # Updated to author__user
    
    gallery_projects = []
    for project in projects:
        gallery_projects.append({
            "title": project.title,
            "author": project.author.user.username if project.author and project.author.user else "Anonymous",  # Updated
            "category": project.category,
            "description": project.description,
            "tech_used": project.tech_used,
            "created_at": project.created_at,
            "views": project.views,
            "likes": project.likes,
            "id": project.id,
            "screenshot": project.screenshot.url if project.screenshot else None
        })
    
    return render(request, 'projects/home_page.html', {
        'projects': projects,
        'gallery_projects': gallery_projects
    })

@login_required
def submit_project(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            description = request.POST.get("description")
            category = request.POST.get("category")
            other_category = request.POST.get("other_category")
            github_url = request.POST.get("github_url")
            live_demo = request.POST.get("live_demo")
            video_demo = request.POST.get("video_demo")
            tech_used = request.POST.get("tech_used")
            screenshot = request.FILES.get("screenshot")

            # Validate required fields
            if not all([title, description, category, github_url, tech_used]):
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'projects/project_form.html')

            # Handle "other" category
            if category == "other" and other_category:
                category = other_category

            # Get or create UserProfile for the current user
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Create project with UserProfile as author
            project = Project.objects.create(
                author=user_profile,
                title=title,
                description=description,
                category=category,
                github_url=github_url,
                live_demo=live_demo or None,
                video_demo=video_demo or None,
                tech_used=tech_used,
                screenshot=screenshot
            )

            messages.success(request, f"Project '{title}' submitted successfully!")
            
            # FORCE REDIRECT TO REGULAR USER PROFILE
            return redirect('/profile/')  # Hardcoded to ensure correct redirect

        except Exception as e:
            messages.error(request, f"Error submitting project: {str(e)}")
            return render(request, 'projects/project_form.html')

    return render(request, 'projects/project_form.html')

def gallery(request):
    projects = Project.objects.all().select_related('author__user')  # Updated to author__user
    return render(request, "projects/gallery.html", {"projects": projects})

@login_required
def user_profile(request):
    # Get the user's UserProfile first
    user_profile = UserProfile.objects.get(user=request.user)
    # Only show projects that belong to the current user's UserProfile
    user_projects = Project.objects.filter(author=user_profile)
    return render(request, 'dashboard/userProfile.html', {
        'projects': user_projects,
        'user': request.user
    })