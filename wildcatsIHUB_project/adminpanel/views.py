from django.shortcuts import render
from datetime import date
from projects.models import Project

def admin_dashboard(request):
    projects = Project.objects.all()
    for project in projects:
        project.badge_class = 'active' if project.status == 'Active' else 'completed'
    return render(request, "adminpanel/admin_dashboard.html", {})

def approvals(request):
    pending_projects = [
        {"title": "New Game", "category": "Game Development", "submitted_by": "Alice", "submitted_at": date(2025, 10, 10)},
        {"title": "Weather App", "category": "Web", "submitted_by": "Bob", "submitted_at": date(2025, 10, 12)},
    ]
    return render(request, "adminpanel/approvals.html", {"pending_projects": pending_projects})

def gallery(request):
    projects = [
        {"title": "Portfolio Website", "image": "project_screenshots/portfolio.png"},
        {"title": "Weather App", "image": "project_screenshots/weather.png"},
    ]
    return render(request, "adminpanel/gallery.html", {"projects": projects})

def submissions(request):
    submissions = [
        {"title": "E-commerce Platform Redesign", "status": "Approved", "author": "John Doe", "date": "2024-03-15", "category": "Web Development", "files": 12, "desc": "Modern UI/UX redesign"},
        {"title": "Mobile Banking Application", "status": "Pending", "author": "Jane Smith", "date": "2024-03-14", "category": "Mobile App", "files": 8, "desc": "Secure transactions with biometrics"},
        {"title": "AI Analytics Dashboard", "status": "Approved", "author": "Mike Johnson", "date": "2024-03-13", "category": "Data Science", "files": 15, "desc": "ML-driven analytics"},
    ]
    stats = {"total": 234, "approved": 189, "rejected": 22, "pending": 23}
    return render(request, "adminpanel/submissions.html", {"submissions": submissions, "stats": stats})

def user_management(request):
    users = [
        {"username": "Alice", "email": "alice@example.com", "role": "Admin", "status": "Active"},
        {"username": "Bob", "email": "bob@example.com", "role": "Staff", "status": "Inactive"},
        {"username": "Charlie", "email": "charlie@example.com", "role": "Staff", "status": "Active"},
    ]
    return render(request, "adminpanel/user_management.html", {"users": users})

def project_tracking(request):
    projects = [
        {"title": "AI Chatbot", "category": "AI / NLP", "status": "Completed", "submitted_by": "Alice", "submitted_at": date(2025,9,28)},
        {"title": "Game Project", "category": "Game Development", "status": "Active", "submitted_by": "Bob", "submitted_at": date(2025,9,19)},
    ]
    return render(request, "adminpanel/project_tracking.html", {"projects": projects})

def admin_profile(request):
    user = {"username": "AdminUser", "email": "admin@example.com", "role": "Admin"}
    return render(request, "adminpanel/admin_profile.html", {"user": user})