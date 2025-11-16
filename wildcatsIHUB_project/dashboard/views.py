from django.shortcuts import render
from datetime import date
from projects.models import Project


def user_profile(request):
    projects = Project.objects.all() 
    return render(request, 'dashboard/userProfile.html', {'projects': projects})

def landing_page(request):
    """Simple landing page view"""
    return render(request, 'dashboard/landing_page.html')

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

    return render(request, "dashboard/dashboard.html", {"projects": projects, "stats": stats})