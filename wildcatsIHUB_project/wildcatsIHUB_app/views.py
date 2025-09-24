from django.shortcuts import render
from .models import Project

def home(request):
    projects = Project.objects.all()
    return render(request, 'wildcatsIHUB_app/home.html', {'projects': projects})

