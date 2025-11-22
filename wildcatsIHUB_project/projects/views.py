from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Add this import
from django.contrib import messages
from .models import Project
from accounts.models import UserProfile
from django.utils import timezone
from datetime import timedelta

@login_required
def view_user_profile(request, user_id):
    """View another user's profile (read-only)"""
    # Get the user being viewed
    viewed_user = get_object_or_404(User, id=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=viewed_user)
    
    # Get the viewed user's projects
    user_projects = Project.objects.filter(author=user_profile).order_by('-created_at')
    
    # Check if this is the current user's own profile
    is_own_profile = (request.user.id == user_id)
    
    context = {
        'viewed_user': viewed_user,
        'viewed_profile': user_profile,
        'projects': user_projects,
        'is_own_profile': is_own_profile,
        'user': request.user  # Current logged in user
    }
    
    return render(request, 'dashboard/view_user_profile.html', context)

def view_project(request, project_id):
    """View individual project details"""
    project = get_object_or_404(Project, id=project_id)
    # Increment view count
    project.views += 1
    project.save()
    return render(request, 'projects/view_project.html', {'project': project})

@login_required
def delete_project(request, project_id):
    """Delete a project (only by owner)"""
    user_profile = UserProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, id=project_id, author=user_profile)
    project_title = project.title
    project.delete()
    messages.success(request, f"Project '{project_title}' deleted successfully!")
    return redirect('userProfile')              

def home(request):
    """Home page with all projects and feed"""
    # Get all projects ordered by creation date (newest first)
    projects = Project.objects.all().select_related('author__user').order_by('-created_at')
    
    # Get recent projects for the feed (last 7 days)
    recent_cutoff = timezone.now() - timedelta(days=7)
    feed_projects = projects.filter(created_at__gte=recent_cutoff)[:10]  # Last 10 projects
    
    # Get user's recent projects for sidebar
    my_recent_projects = Project.objects.none()
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            my_recent_projects = Project.objects.filter(author=user_profile).order_by('-created_at')[:6]
        except UserProfile.DoesNotExist:
            pass
    
    # Get trending projects (most viewed in last 30 days)
    trending_cutoff = timezone.now() - timedelta(days=30)
    trending_projects = Project.objects.filter(
        created_at__gte=trending_cutoff
    ).order_by('-views')[:5]
    
    # Format projects for the gallery
    gallery_projects = []
    for project in projects:
        gallery_projects.append({
            "title": project.title,
            "author": project.author.user.username if project.author and project.author.user else "Anonymous",
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
        'gallery_projects': gallery_projects,
        'feed_projects': feed_projects,
        'trending_projects': trending_projects,
        'my_recent_projects': my_recent_projects  # Add this line
    })

@login_required
def submit_project(request):
    """Submit a new project"""
    if request.method == "POST":
        try:
            # Get form data
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            category = request.POST.get("category", "").strip()
            other_category = request.POST.get("other_category", "").strip()
            github_url = request.POST.get("github_url", "").strip()
            live_demo = request.POST.get("live_demo", "").strip()
            video_demo = request.POST.get("video_demo", "").strip()
            tech_used = request.POST.get("tech_used", "").strip()
            screenshot = request.FILES.get("screenshot")

            # Validate required fields
            if not title or not description or not category or not github_url or not tech_used:
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'projects/project_form.html', {'request': request})

            # Handle "other" category
            if category == "other":
                if not other_category:
                    messages.error(request, "Please specify the category when selecting 'Other'.")
                    return render(request, 'projects/project_form.html', {'request': request})
                category = other_category

            # Validate GitHub URL format
            if not github_url.startswith(('http://', 'https://')):
                messages.error(request, "Please enter a valid GitHub URL.")
                return render(request, 'projects/project_form.html', {'request': request})

            # Get or create UserProfile for the current user
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Create project
            project = Project.objects.create(
                author=user_profile,
                title=title,
                description=description,
                category=category,
                github_url=github_url,
                live_demo=live_demo if live_demo else None,
                video_demo=video_demo if video_demo else None,
                tech_used=tech_used,
                screenshot=screenshot
            )

            messages.success(request, f"Project '{title}' submitted successfully!")
            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)

        except Exception as e:
            messages.error(request, f"Error submitting project: {str(e)}")
            return render(request, 'projects/project_form.html', {'request': request})

    return render(request, 'projects/project_form.html')

def gallery(request):
    """Project gallery view"""
    projects = Project.objects.all().select_related('author__user').order_by('-created_at')
    return render(request, "projects/gallery.html", {"projects": projects})

@login_required
def user_profile(request):
    """User profile with their projects"""
    user_profile = UserProfile.objects.get(user=request.user)
    user_projects = Project.objects.filter(author=user_profile).order_by('-created_at')
    return render(request, 'userProfile.html', {
        'projects': user_projects,
        'user': request.user
    })

@login_required
def edit_project(request, project_id):
    """Edit an existing project"""
    user_profile = UserProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, id=project_id, author=user_profile)
    
    if request.method == "POST":
        try:
            # Get form data
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()
            category = request.POST.get("category", "").strip()
            other_category = request.POST.get("other_category", "").strip()
            github_url = request.POST.get("github_url", "").strip()
            live_demo = request.POST.get("live_demo", "").strip()
            video_demo = request.POST.get("video_demo", "").strip()
            tech_used = request.POST.get("tech_used", "").strip()

            # Validate required fields
            if not title or not description or not category or not github_url or not tech_used:
                messages.error(request, "Please fill in all required fields.")
                return render(request, 'projects/project_form.html', {
                    'project': project,
                    'editing': True
                })

            # Handle "other" category
            if category == "other":
                if not other_category:
                    messages.error(request, "Please specify the category when selecting 'Other'.")
                    return render(request, 'projects/project_form.html', {
                        'project': project,
                        'editing': True
                    })
                category = other_category

            # Validate GitHub URL format
            if not github_url.startswith(('http://', 'https://')):
                messages.error(request, "Please enter a valid GitHub URL.")
                return render(request, 'projects/project_form.html', {
                    'project': project,
                    'editing': True
                })

            # Update project fields
            project.title = title
            project.description = description
            project.category = category
            project.github_url = github_url
            project.live_demo = live_demo if live_demo else None
            project.video_demo = video_demo if video_demo else None
            project.tech_used = tech_used
            
            # Handle new screenshot upload (only if file is provided)
            if 'screenshot' in request.FILES and request.FILES['screenshot']:
                project.screenshot = request.FILES['screenshot']
            
            project.save()
            messages.success(request, f"Project '{project.title}' updated successfully!")
            return redirect('view_project', project_id=project.id)
            
        except Exception as e:
            messages.error(request, f"Error updating project: {str(e)}")
            return render(request, 'projects/project_form.html', {
                'project': project,
                'editing': True
            })
    
    # Pre-fill the form with existing project data
    context = {
        'project': project,
        'editing': True
    }
    return render(request, 'projects/project_form.html', context)