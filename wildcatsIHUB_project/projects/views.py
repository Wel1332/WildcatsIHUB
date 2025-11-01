from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from accounts.models import UserProfile

def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/view_project.html', {'project': project})

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('user_profile')

def home(request):
    projects = Project.objects.all()
    
    gallery_projects = []
    for project in projects:
        gallery_projects.append({
            "title": project.title,
            "author": project.author.user.username if project.author else "Anonymous",
            "category": project.category,
            "description": project.description,
            "tech_used": project.tech_used,
            "created_at": project.created_at,
            "views": project.views or 0,
            "likes": project.likes or 0,
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
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        other_category = request.POST.get("other_category")
        github_url = request.POST.get("github_url")
        live_demo = request.POST.get("live_demo")
        video_demo = request.POST.get("video_demo")
        tech_used = request.POST.get("tech_used")
        screenshot = request.FILES.get("screenshot")

        if category == "other" and other_category:
            category = other_category

        user_profile = UserProfile.objects.get(user=request.user)

        Project.objects.create(
            title=title,
            description=description,
            category=category,
            github_url=github_url,
            live_demo=live_demo,
            video_demo=video_demo,
            tech_used=tech_used,
            screenshot=screenshot,
            author=user_profile 
        )

        return redirect('user_profile')

    return render(request, 'projects/project_form.html')

def gallery(request):
    projects = [
        {"title": "Portfolio Website", "image": "project_screenshots/portfolio.png"},
        {"title": "Weather App", "image": "project_screenshots/weather.png"},
    ]
    return render(request, "projects/gallery.html", {"projects": projects})