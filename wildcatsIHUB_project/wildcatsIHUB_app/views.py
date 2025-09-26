from django.shortcuts import render, redirect
from .models import Project

def home(request):
    projects = Project.objects.all()
    return render(request, 'wildcatsIHUB_app/home.html', {'projects': projects})

def submit_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        github_url = request.POST.get("github_url")
        live_demo = request.POST.get("live_demo")
        video_demo = request.POST.get("video_demo")
        tech_used = request.POST.get("tech_used")
        screenshot = request.FILES.get("screenshot")

        # Save project to DB
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

        return redirect('home')  # after submission go back to home page

    return render(request, 'wildcatsIHUB_app/project_form.html')
