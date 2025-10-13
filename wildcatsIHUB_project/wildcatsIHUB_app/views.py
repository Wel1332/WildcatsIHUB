from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from datetime import date
from django.shortcuts import get_object_or_404 
import json
from .forms import StudentLoginForm  # Import your custom form

def login_view(request):
    # Use your custom StudentLoginForm instead of AuthenticationForm
    form = StudentLoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')  # or your dashboard URL
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

def home(request):
    projects = Project.objects.all()
    
    gallery_projects = []
    for project in projects:
        gallery_projects.append({
            "title": project.title,
            "author": project.user.username if project.user else "Anonymous",
            "category": project.category,
            "description": project.description,
            "tech_used": project.tech_used,
            "created_at": project.created_at,
            "views": project.views or 0,
            "likes": project.likes or 0,
            "id": project.id,
            "screenshot": project.screenshot.url if project.screenshot else None
        })
    
    return render(request, 'wildcatsIHUB_app/home_page.html', {
        'projects': projects,
        'gallery_projects': gallery_projects
    })


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

def admin_dashboard(request):
    context = {
        "total_users": 1234,
        "pending_approvals": 23,
        "approved_projects": 456,
        "active_projects": 89,
        "project_data": json.dumps([45, 52, 47, 61, 54, 67]),
        "months": json.dumps(["Jan", "Feb", "Mar", "Apr", "May", "Jun"]),
    }
    return render(request, "wildcatsIHUB_app/admin_dashboard.html", context)


def user_management(request):
    users = [
        {"name": "John Doe", "email": "john@example.com", "role": "User", "status": "Active", "projects": 5, "joined": "2024-01-15"},
        {"name": "Jane Smith", "email": "jane@example.com", "role": "User", "status": "Pending", "projects": 0, "joined": "2024-03-20"},
        {"name": "Mike Johnson", "email": "mike@example.com", "role": "Admin", "status": "Active", "projects": 12, "joined": "2023-11-05"},
    ]
    return render(request, "wildcatsIHUB_app/user_management.html", {"users": users})


def approval_system(request):
    projects = [
        {"title": "E-commerce Platform Redesign", "category": "Web Development", "author": "John Doe", "date": "2024-03-15", "desc": "A complete redesign with modern UI/UX principles"},
        {"title": "Mobile Banking App", "category": "Mobile App", "author": "Jane Smith", "date": "2024-03-14", "desc": "Secure banking app with biometric authentication"},
        {"title": "AI-Powered Analytics Dashboard", "category": "Data Science", "author": "Mike Johnson", "date": "2024-03-13", "desc": "AI-driven analytics dashboard"},
    ]
    return render(request, "wildcatsIHUB_app/approvals.html", {"projects": projects})


def project_tracking(request):
    projects = [
        {"title": "E-commerce Platform", "owner": "John Doe", "category": "Web Development", "status": "Approved", "progress": 75, "updated": "2024-03-10"},
        {"title": "Mobile Banking App", "owner": "Jane Smith", "category": "Mobile App", "status": "Pending", "progress": 30, "updated": "2024-03-12"},
        {"title": "Analytics Dashboard", "owner": "Mike Johnson", "category": "Data Science", "status": "Approved", "progress": 90, "updated": "2024-03-14"},
    ]
    return render(request, "wildcatsIHUB_app/project_tracking.html", {"projects": projects})


def submissions(request):
    submissions = [
        {"title": "E-commerce Platform Redesign", "status": "Approved", "author": "John Doe", "date": "2024-03-15", "category": "Web Development", "files": 12, "desc": "Modern UI/UX redesign"},
        {"title": "Mobile Banking Application", "status": "Pending", "author": "Jane Smith", "date": "2024-03-14", "category": "Mobile App", "files": 8, "desc": "Secure transactions with biometrics"},
        {"title": "AI Analytics Dashboard", "status": "Approved", "author": "Mike Johnson", "date": "2024-03-13", "category": "Data Science", "files": 15, "desc": "ML-driven analytics"},
    ]
    stats = {"total": 234, "approved": 189, "rejected": 22, "pending": 23}
    return render(request, "wildcatsIHUB_app/submissions.html", {"submissions": submissions, "stats": stats})


def project_gallery(request):
    gallery = [
        {"title": "E-commerce Platform", "author": "John Doe", "category": "Web Development", "likes": 124, "comments": 23, "views": 1543},
        {"title": "Mobile Banking App", "author": "Jane Smith", "category": "Mobile App", "likes": 98, "comments": 15, "views": 987},
        {"title": "Analytics Dashboard", "author": "Mike Johnson", "category": "Data Science", "likes": 156, "comments": 31, "views": 2134},
    ]
    return render(request, "wildcatsIHUB_app/gallery.html", {"gallery": gallery})


def profile_settings(request):
    profile = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "bio": "",
    }
    return render(request, "wildcatsIHUB_app/admin_profile.html", {"profile": profile})