from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from datetime import date
from django.shortcuts import get_object_or_404


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('/')
    return render(request, 'wildcatsIHUB_app/login.html', {'form': form})

def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'wildcatsIHUB_app/view_project.html', {'project': project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('user_profile')



def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'wildcatsIHUB_app/signup.html', {'form': form})

def home(request):
    projects = Project.objects.all()
    return render(request, 'wildcatsIHUB_app/home.html', {'projects': projects})

def submit_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        other_category = request.POST.get("other_category")  # <-- add this
        github_url = request.POST.get("github_url")
        live_demo = request.POST.get("live_demo")
        video_demo = request.POST.get("video_demo")
        tech_used = request.POST.get("tech_used")
        screenshot = request.FILES.get("screenshot")

        # Use 'other_category' if 'category' is 'other'
        if category == "other" and other_category:
            category = other_category

        Project.objects.create(
            title=title,
            description=description,
            category=category,
            github_url=github_url,
            live_demo=live_demo,
            video_demo=video_demo,
            tech_used=tech_used,
            screenshot=screenshot
        )

        return redirect('user_profile')

    return render(request, 'wildcatsIHUB_app/project_form.html')


def user_profile(request):
    projects = Project.objects.all() 
    return render(request, 'wildcatsIHUB_app/userProfile.html', {'projects': projects})


def landing_page(request):
    """Simple landing page view"""
    return render(request, 'wildcatsIHUB_app/landing_page.html')

def dashboard(request):
    
    # mock data (replace with real DB query later)
    projects = [
        {
            "title": "dan",
            "description": "asdadas",
            "category": "Game Development",
            "status": "active",
            "views": 3,
            "created_at": date(2025, 9, 19),
            "tech_stack": ["python"],
        },
        {
            "title": "AI Chatbot",
            "description": "A Django + React chatbot app",
            "category": "AI / NLP",
            "status": "completed",
            "views": 12,
            "created_at": date(2025, 9, 28),
            "tech_stack": ["python", "react"],
        },
    ]

    stats = {
        "total_projects": len(projects),
        "total_views": sum(p["views"] for p in projects),
        "active_projects": sum(1 for p in projects if p["status"] == "active"),
        "growth": "+12%",  # placeholder
    }

    return render(request, "wildcatsIHUB_app/dashboard.html", {"projects": projects, "stats": stats})

   
