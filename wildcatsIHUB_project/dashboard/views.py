from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from accounts.models import UserProfile


@login_required
def user_profile(request):
    projects = Project.objects.all() 
    return render(request, 'dashboard/userProfile.html', {'projects': projects})

def landing_page(request):
    """Simple landing page view"""
    return render(request, 'dashboard/landing_page.html')

@login_required
def dashboard(request):
    """User dashboard with project statistics"""
    # Try multiple ways to get user's projects
    user_projects = Project.objects.none()
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Try different field names that might link projects to user
        if Project.objects.filter(author=user_profile).exists():
            user_projects = Project.objects.filter(author=user_profile).order_by('-created_at')
        elif Project.objects.filter(created_by=user_profile).exists():
            user_projects = Project.objects.filter(created_by=user_profile).order_by('-created_at')
        elif Project.objects.filter(user=request.user).exists():
            user_projects = Project.objects.filter(user=request.user).order_by('-created_at')
        elif Project.objects.filter(owner=request.user).exists():
            user_projects = Project.objects.filter(owner=request.user).order_by('-created_at')
        else:
            # If no specific relationship found, get all projects (for testing)
            user_projects = Project.objects.all().order_by('-created_at')
            
    except UserProfile.DoesNotExist:
        # If no UserProfile, try direct user relationships
        if Project.objects.filter(user=request.user).exists():
            user_projects = Project.objects.filter(user=request.user).order_by('-created_at')
        elif Project.objects.filter(owner=request.user).exists():
            user_projects = Project.objects.filter(owner=request.user).order_by('-created_at')
        else:
            user_projects = Project.objects.all().order_by('-created_at')
    
    # Calculate basic statistics
    total_projects = user_projects.count()
    
    # Recent submissions (last 30 days)
    recent_submissions = user_projects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Calculate total technologies used (handle empty tech_used)
    all_techs = []
    for project in user_projects:
        if project.tech_used:
            # Handle both comma-separated and space-separated tech lists
            techs = [tech.strip() for tech in project.tech_used.replace(',', ' ').split() if tech.strip()]
            all_techs.extend(techs)
    total_technologies = len(set(all_techs)) if all_techs else 0
    
    # Get project categories and count unique ones
    category_mapping = {
        'web': 'Web Development',
        'mobile': 'Mobile Development', 
        'desktop': 'Desktop Application',
        'ai': 'Artificial Intelligence',
        'data': 'Data Science',
        'game': 'Game Development',
        'ml': 'Machine Learning',
        'iot': 'Internet of Things',
        'cloud': 'Cloud Computing',
        'other': 'Other',
    }
    
    project_categories = []
    for project in user_projects:
        if project.category:
            display_category = category_mapping.get(project.category, project.category.title())
            project_categories.append(display_category)
    
    unique_categories = list(set(project_categories))
    total_categories = len(unique_categories)
    
    # Get most viewed project
    most_viewed_project = user_projects.order_by('-views').first()
    
    # Get latest project
    latest_project = user_projects.first()
    
    # Calculate engagement score (based on project count and diversity)
    if total_projects > 0:
        engagement_score = min(100, total_projects * 20 + total_categories * 15)
    else:
        engagement_score = 0
        
    if engagement_score >= 80:
        engagement_status = "Excellent"
    elif engagement_score >= 50:
        engagement_status = "Good"
    else:
        engagement_status = "Getting Started"
    
    context = {
        'user_projects': user_projects, 
        'total_projects': total_projects,
        'submitted_projects': total_projects, 
        'recent_submissions': recent_submissions,
        'total_technologies': total_technologies,
        'project_categories': unique_categories,  
        'unique_categories': unique_categories,  
        'total_categories': total_categories,    
        'most_viewed_project': most_viewed_project,
        'latest_project': latest_project,
        'engagement_score': engagement_score,
        'engagement_status': engagement_status,
    }
    
    return render(request, 'dashboard/dashboard.html', context)