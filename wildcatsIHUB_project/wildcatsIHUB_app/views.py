from django.shortcuts import render, redirect
from .models import Project
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from datetime import date
from django.shortcuts import get_object_or_404 
import json
from .forms import StudentLoginForm  
from django.db import IntegrityError
from django.contrib import messages
from supabase import create_client
import os
from .models import UserProfile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            result = supabase.auth.resend({
                "type": "signup",
                "email": email,
            })
        
            return render(request, 'wildcatsIHUB_app/signup.html', {
                'success_message': '✅ Verification email resent! Please check your inbox and spam folder.',
                'resend_email': email
            })
        except Exception as e:
            return render(request, 'wildcatsIHUB_app/signup.html', {
                'error': f'Failed to resend verification: {str(e)}'
            })

    return redirect('signup')


@require_POST
@csrf_exempt
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required'})
        
        # Check if it's a .edu email
        if not email.endswith('.edu'):
            return JsonResponse({'success': False, 'error': 'Please use a valid .edu email address'})
        
        # Send reset password email via Supabase
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        # Check if user exists in Supabase first
        users = supabase.auth.admin.list_users()
        user_exists = False
        target_user = None
        
        for user in users:
            if user.email == email:
                user_exists = True
                target_user = user
                break
        
        if not user_exists:
            return JsonResponse({'success': False, 'error': 'No account found with this email address. Please sign up first.'})
        
        # Check if email is confirmed
        if target_user and not target_user.email_confirmed_at:
            return JsonResponse({'success': False, 'error': 'Please verify your email address before resetting your password.'})
        
        # This will send a password reset email to the user
        result = supabase.auth.reset_password_for_email(email)
        
        # Check if there was an error from Supabase
        if hasattr(result, 'error') and result.error:
            error_msg = str(result.error)
            if "User not allowed" in error_msg:
                return JsonResponse({'success': False, 'error': 'Cannot reset password. Please verify your email first or contact support.'})
            else:
                return JsonResponse({'success': False, 'error': error_msg})
        
        return JsonResponse({'success': True, 'message': 'Password reset link has been sent to your email'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # 1. Try to authenticate with Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "email": email, 
                "password": password
            })
            
            # 2. If Supabase authentication succeeds
            if auth_response.user:
                # Get or create Django user (don't check Django password)
                from django.contrib.auth.models import User
                
                try:
                    django_user = User.objects.get(username=email)
                    # Activate if not active
                    if not django_user.is_active:
                        django_user.is_active = True
                        django_user.save()
                except User.DoesNotExist:
                    # Create user without setting password in Django
                    django_user = User.objects.create_user(
                        username=email,
                        email=email,
                        password="temp_password_123"  # Dummy password
                    )
                    django_user.is_active = True
                    django_user.save()
                
                # 3. Login the user to Django (bypass Django auth)
                django_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, django_user)
                return redirect('home')
                
        except Exception as e:
            error_msg = str(e)
            if "Email not confirmed" in error_msg:
                messages.error(request, "Please verify your email address before logging in.")
            elif "Invalid login credentials" in error_msg:
                messages.error(request, "Incorrect email or password. Please try again.")
            else:
                messages.error(request, f"Login failed: {error_msg}")
    
    form = StudentLoginForm()
    return render(request, 'wildcatsIHUB_app/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        year_level = request.POST.get('year_level')
        
        from django.contrib.auth.models import User
        from .models import UserProfile
        
        try:
            # Initialize Supabase client
            supabase = create_client(
                os.getenv('SUPABASE_URL'),
                os.getenv('SUPABASE_KEY')
            )
            
            # Check if email already exists in Django
            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                error_msg = 'Email already registered! Please use a different email or login.'
                return render(request, 'wildcatsIHUB_app/signup.html', {'error': error_msg})
            
            # Check if student ID already exists
            if UserProfile.objects.filter(student_id=student_id).exists():
                error_msg = 'Student ID already exists! Please use a different Student ID.'
                return render(request, 'wildcatsIHUB_app/signup.html', {'error': error_msg})
            
            # Create Supabase user FIRST (this sends verification email)
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "student_id": student_id
                    }
                }
            })
            
            # Check if Supabase user was created successfully
            if hasattr(auth_response, 'user') and auth_response.user:
                # Create Django user only after Supabase success
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True 
                )
                
                UserProfile.objects.create(
                    user=user,
                    student_id=student_id,
                    department=department,
                    year_level=year_level
                )
                
                success_message = '✅ Account created successfully! Please check your email (including spam folder) for the verification link. You must verify your email before you can login.'
                return render(request, 'wildcatsIHUB_app/signup.html', {
                    'success_message': success_message
                })
            else:
                error_msg = 'Failed to create authentication account. Please try again.'
                return render(request, 'wildcatsIHUB_app/signup.html', {'error': error_msg})
                
        except IntegrityError as e:
            # Clean up any partially created users
            try:
                User.objects.filter(username=email).delete()
            except:
                pass
                
            if 'student_id' in str(e):
                error_msg = 'Student ID already exists! Please use a different Student ID.'
            else:
                error_msg = 'This user already exists! Please use different information.'
            
            return render(request, 'wildcatsIHUB_app/signup.html', {'error': error_msg})
            
        except Exception as e:
            # Clean up any partially created users
            try:
                User.objects.filter(username=email).delete()
            except:
                pass
                
            error_msg = f'Error creating account: {str(e)}'
            return render(request, 'wildcatsIHUB_app/signup.html', {'error': error_msg})
    
    return render(request, 'wildcatsIHUB_app/signup.html')



def view_project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'wildcatsIHUB_app/view_project.html', {'project': project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('user_profile')


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
    projects = Project.objects.all()
    for project in projects:
        project.badge_class = 'active' if project.status == 'Active' else 'completed'
    context = {
        'projects': projects,
    }

    return render(request, "wildcatsIHUB_app/admin_dashboard.html", {
    })

# --- Approvals ---
def approvals(request):
    pending_projects = [
        {"title": "New Game", "category": "Game Development", "submitted_by": "Alice", "submitted_at": date(2025, 10, 10)},
        {"title": "Weather App", "category": "Web", "submitted_by": "Bob", "submitted_at": date(2025, 10, 12)},
    ]
    return render(request, "wildcatsIHUB_app/approvals.html", {"pending_projects": pending_projects})

def submissions(request):
    submissions = [
        {"title": "E-commerce Platform Redesign", "status": "Approved", "author": "John Doe", "date": "2024-03-15", "category": "Web Development", "files": 12, "desc": "Modern UI/UX redesign"},
        {"title": "Mobile Banking Application", "status": "Pending", "author": "Jane Smith", "date": "2024-03-14", "category": "Mobile App", "files": 8, "desc": "Secure transactions with biometrics"},
        {"title": "AI Analytics Dashboard", "status": "Approved", "author": "Mike Johnson", "date": "2024-03-13", "category": "Data Science", "files": 15, "desc": "ML-driven analytics"},
    ]
    stats = {"total": 234, "approved": 189, "rejected": 22, "pending": 23}
    return render(request, "wildcatsIHUB_app/submissions.html", {"submissions": submissions, "stats": stats})

# --- Users ---
def user_management(request):
    users = [
        {"username": "Alice", "email": "alice@example.com", "role": "Admin", "status": "Active"},
        {"username": "Bob", "email": "bob@example.com", "role": "Staff", "status": "Inactive"},
        {"username": "Charlie", "email": "charlie@example.com", "role": "Staff", "status": "Active"},
    ]
    return render(request, "wildcatsIHUB_app/user_management.html", {"users": users})

# --- Project Tracking ---
def project_tracking(request):
    projects = [
        {"title": "AI Chatbot", "category": "AI / NLP", "status": "Completed", "submitted_by": "Alice", "submitted_at": date(2025,9,28)},
        {"title": "Game Project", "category": "Game Development", "status": "Active", "submitted_by": "Bob", "submitted_at": date(2025,9,19)},
    ]
    return render(request, "wildcatsIHUB_app/project_tracking.html", {"projects": projects})

# --- Gallery ---
def gallery(request):
    projects = [
        {"title": "Portfolio Website", "image": "project_screenshots/portfolio.png"},
        {"title": "Weather App", "image": "project_screenshots/weather.png"},
    ]
    return render(request, "wildcatsIHUB_app/gallery.html", {"projects": projects})

# --- Profile ---
def admin_profile(request):
    user = {"username": "AdminUser", "email": "admin@example.com", "role": "Admin"}
    return render(request, "wildcatsIHUB_app/admin_profile.html", {"user": user})

