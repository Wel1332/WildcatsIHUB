from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import Announcement
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from accounts.models import UserProfile
from django.http import JsonResponse
import supabase
from django.conf import settings
import os

supabase_client = supabase.create_client(
    'https://pizsazxthvvavhdbowzi.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpenNhenh0aHZ2YXZoZGJvd3ppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAzMjU2OTQsImV4cCI6MjA3NTkwMTY5NH0.FHp8TwLPGp_aARF3uqVZVrG3dWbvd1H18O0Wiikweyg'
)

@login_required
def user_profile(request):
    """User profile - FIXED with correct field names"""
    user = request.user
    
    # Get from Supabase
    supabase_data = get_user_profile_from_supabase(user.id)
    
    if supabase_data:
        # Use EXACT field names from Supabase JSON
        context = {
            # These fields HAVE DATA in Supabase
            'user_name': supabase_data.get('full_name', ''),
            'user_title': supabase_data.get('title', ''),
            'user_school': supabase_data.get('school', ''),
            'user_year': supabase_data.get('year_level', ''),
            'user_location': supabase_data.get('location', ''),
            'user_graduation': supabase_data.get('graduation_year', ''),  # USE graduation_year NOT graduation_yr
            'user_about': supabase_data.get('about', ''),
            'user_interests': supabase_data.get('interests', ''),
            
            # These fields are NULL in Supabase (will show as empty)
            'user_student_id': supabase_data.get('student_id', ''),
            'user_department': supabase_data.get('department', ''),
            'user_specialization': supabase_data.get('specialization', ''),
            'user_major': supabase_data.get('major', ''),
            'user_minor': supabase_data.get('minor', ''),
            'user_courses': supabase_data.get('courses', ''),
        }
    else:
        # Fallback if no Supabase data
        context = {
            'user_name': user.get_full_name() or user.username,
            'user_title': '',
            'user_school': '',
            'user_year': '',
            'user_location': '',
            'user_graduation': '',
            'user_about': '',
            'user_interests': '',
            'user_student_id': '',
            'user_department': '',
            'user_specialization': '',
            'user_major': '',
            'user_minor': '',
            'user_courses': '',
        }
    
    # Get projects
    projects = get_user_projects_django(user)
    context['projects'] = projects
    context['projects_count'] = projects.count()
    
    print(f"🔥 DEBUG - Data being sent to template:")
    print(f"🔥 Name: {context.get('user_name')}")
    print(f"🔥 School: {context.get('user_school')}")
    print(f"🔥 Year: {context.get('user_year')}")
    print(f"🔥 Graduation: {context.get('user_graduation')}")  # This should now show "2026"
    print(f"🔥 Location: {context.get('user_location')}")
    print(f"🔥 About: {context.get('user_about')}")
    
    return render(request, 'dashboard/userProfile.html', context)
    """User profile - FIXED with correct Supabase mapping"""
    user = request.user
    
    # Get from Supabase
    supabase_data = get_user_profile_from_supabase(user.id)
    
    if supabase_data:
        # Map Supabase columns to template variables
        context = {
            # These are WORKING (from your screenshot)
            'user_name': supabase_data.get('full_name', ''),
            'user_school': supabase_data.get('school', ''),
            'user_year': supabase_data.get('year_level', ''),
            'user_location': supabase_data.get('location', ''),
            'user_graduation': supabase_data.get('graduation_yr', ''),  # This is 'graduation_yr' not 'graduation_year'
            'user_about': supabase_data.get('about', ''),
            'user_interests': supabase_data.get('interests', ''),
            
            # These might be EMPTY in Supabase
            'user_title': supabase_data.get('title', ''),
            'user_specialization': supabase_data.get('specialization', ''),
            'user_major': supabase_data.get('major', ''),
            'user_minor': supabase_data.get('minor', ''),
            'user_courses': supabase_data.get('courses', ''),
            
            # These are DIFFERENT column names in Supabase
            'user_student_id': supabase_data.get('student_id', ''),  # Changed from 'student_id'
            'user_department': supabase_data.get('department', ''),  # Changed from 'department'
        }
    else:
        # Default empty values if no Supabase data
        context = {
            'user_name': user.get_full_name() or user.username,
            'user_school': '',
            'user_year': '',
            'user_location': '',
            'user_graduation': '',
            'user_about': '',
            'user_interests': '',
            'user_title': '',
            'user_specialization': '',
            'user_major': '',
            'user_minor': '',
            'user_courses': '',
            'user_student_id': '',
            'user_department': '',
        }
    
    # Get projects
    projects = get_user_projects_django(user)
    context['projects'] = projects
    context['projects_count'] = projects.count()
    
    # DEBUG: Print what we're sending
    print(f"🔥 SUPABASE DATA FOUND: {bool(supabase_data)}")
    print(f"🔥 Name: {context.get('user_name')}")
    print(f"🔥 School: {context.get('user_school')}")
    print(f"🔥 Graduation: {context.get('user_graduation')}")
    print(f"🔥 Student ID: {context.get('user_student_id')}")
    print(f"🔥 Department: {context.get('user_department')}")
    
    return render(request, 'dashboard/userProfile.html', context)

@login_required
def debug_user_data(request):
    """Simple view to see what user data exists"""
    user = request.user
    
    print(f"=== DEBUG USER DATA ===")
    print(f"User ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"First Name: {user.first_name}")
    print(f"Last Name: {user.last_name}")
    print(f"Full Name: {user.get_full_name()}")
    
    # Try to get Django UserProfile (from accounts app)
    try:
        from accounts.models import UserProfile
        profile = UserProfile.objects.get(user=user)
        print(f"Django UserProfile found:")
        print(f"  - Student ID: {profile.student_id}")
        print(f"  - Department: {profile.department}")
        print(f"  - Year Level: {profile.year_level}")
    except ImportError:
        print("Could not import UserProfile from accounts")
    except UserProfile.DoesNotExist:
        print(f"No Django UserProfile found")
    
    # Also check Supabase data
    try:
        supabase_data = get_user_profile_from_supabase(user.id)
        print(f"Supabase data: {supabase_data}")
    except Exception as e:
        print(f"Supabase error: {e}")
    
    # Show this in browser too
    context = {
        'debug_user': user,
        'debug_profile': None,
        'supabase_data': None,
    }
    
    try:
        from accounts.models import UserProfile
        context['debug_profile'] = UserProfile.objects.get(user=user)
    except:
        pass
    
    try:
        context['supabase_data'] = get_user_profile_from_supabase(user.id)
    except:
        pass
    
    return render(request, 'dashboard/debug_user_data.html', context)

def get_user_profile_from_supabase(user_id):
    try:
        print(f"🔥 Fetching Supabase profile for user_id: {user_id} (type: {type(user_id)})")
        
        # Convert to string for Supabase
        user_id_str = str(user_id)
        
        response = supabase_client.table('accounts_userprofile') \
            .select('*') \
            .eq('user_id', user_id_str) \
            .execute()
        
        print(f"🔥 Supabase response: Found {len(response.data) if response.data else 0} records")
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        return None
        
    except Exception as e:
        print(f"🔥 Error fetching from Supabase: {e}")
        return None


def get_user_projects_supabase(user_id):
    try:
        response = supabase_client.table('projects_project') \
            .select('*') \
            .eq('user_id', str(user_id)) \
            .order('created_at', desc=True) \
            .execute()
        
        return response.data
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return None

@login_required
def view_all_supabase_data(request):
    """See ALL data in Supabase for current user"""
    user = request.user
    supabase_data = get_user_profile_from_supabase(user.id)
    
    return JsonResponse({
        'user_id': user.id,
        'username': user.username,
        'supabase_data_exists': bool(supabase_data),
        'supabase_data': supabase_data,
        'all_keys': list(supabase_data.keys()) if supabase_data else []
    })



@login_required
def user_profile(request):
    """User profile view - COMBINED VERSION"""
    try:
        user = request.user
        
        # Get Supabase data
        supabase_data = get_user_profile_from_supabase(user.id)
        
        # Get profile data
        if supabase_data:
            context = {
                'user_name': supabase_data.get('full_name', ''),
                'user_title': supabase_data.get('title', ''),
                'user_school': supabase_data.get('school', ''),
                'user_year': supabase_data.get('year_level', ''),
                'user_location': supabase_data.get('location', ''),
                'user_graduation': supabase_data.get('graduation_year', ''),  # graduation_year NOT graduation_yr
                'user_about': supabase_data.get('about', ''),
                'user_specialization': supabase_data.get('specialization', ''),
                'user_major': supabase_data.get('major', ''),
                'user_minor': supabase_data.get('minor', ''),
                'user_courses': supabase_data.get('courses', ''),
                'user_interests': supabase_data.get('interests', ''),
            }
        else:
            # Defaults if no Supabase data
            context = {
                'user_name': user.get_full_name() or user.username,
                'user_title': '',
                'user_school': '',
                'user_year': '',
                'user_location': '',
                'user_graduation': '',
                'user_about': '',
                'user_specialization': '',
                'user_major': '',
                'user_minor': '',
                'user_courses': '',
                'user_interests': '',
            }
        
        # Get projects from Django database
        try:
            user_profile_obj = UserProfile.objects.get(user=user)
            user_projects = Project.objects.filter(author=user_profile_obj).order_by('-created_at')
            context['projects'] = user_projects
            context['projects_count'] = user_projects.count()
        except UserProfile.DoesNotExist:
            context['projects'] = []
            context['projects_count'] = 0
        
        return render(request, 'dashboard/userProfile.html', context)
        
    except Exception as e:
        print(f"Error in user_profile: {e}")
        return render(request, 'dashboard/userProfile.html', {
            'user_name': request.user.username,
            'projects': [],
            'projects_count': 0,
        })

@login_required
def save_project_to_supabase(request):
    if request.method == 'POST':
        try:
            user_id = str(request.user.id)
            project_data = {
                'user_id': user_id,
                'title': request.POST.get('projectName', ''),
                'description': request.POST.get('projectDescription', ''),
                'tech_used': request.POST.get('projectLanguages', ''),
                'github_url': request.POST.get('projectLink', ''),
                'live_demo': request.POST.get('projectLink', ''),
                'category': 'Software',
                'status': 'completed',
                'created_at': timezone.now().isoformat()
            }
            
            response = supabase_client.table('projects_project') \
                .insert([project_data]) \
                .execute()
            
            return JsonResponse({'success': True, 'message': 'Project saved successfully!'})
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return JsonResponse({'success': False, 'message': 'Error saving project.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def get_supabase_profile_data(request):
    try:
        user_id = str(request.user.id)
        user = request.user
        profile_data = get_user_profile_from_supabase(user_id)
        
        user_full_name = user.get_full_name() or user.username
        
        if profile_data:
            profile_data['full_name'] = profile_data.get('full_name') or user_full_name
            return JsonResponse({'success': True, 'data': profile_data})
        else:
            default_data = {
                'full_name': user_full_name,
                'title': '',
                'school': '',
                'year_level': '',
                'location': '',
                'graduation_year': '',
                'about': '',
                'specialization': '',
                'major': '',
                'minor': '',
                'courses': '',
                'interests': ''
            }
            return JsonResponse({'success': True, 'data': default_data})
            
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        user_full_name = request.user.get_full_name() or request.user.username
        default_data = {
            'full_name': user_full_name,
            'title': '',
            'school': '',
            'year_level': '',
            'location': '',
            'graduation_year': '',
            'about': '',
            'specialization': '',
            'major': '',
            'minor': '',
            'courses': '',
            'interests': ''
        }
        return JsonResponse({'success': True, 'data': default_data})

@login_required
def get_supabase_profile_data(request):
    try:
        user_id = str(request.user.id)
        user = request.user
        profile_data = get_user_profile_from_supabase(user_id)
        
        user_full_name = user.get_full_name() or user.username
        
        if profile_data:
            # Use correct field mapping
            response_data = {
                'full_name': profile_data.get('full_name') or user_full_name,
                'title': profile_data.get('title', ''),
                'school': profile_data.get('school', ''),
                'year_level': profile_data.get('year_level', ''),  # Correct field name
                'location': profile_data.get('location', ''),
                'graduation_yr': profile_data.get('graduation_yr', ''),  # Correct field name
                'about': profile_data.get('about', ''),
                'specialization': profile_data.get('specialization', ''),
                'major': profile_data.get('major', ''),
                'minor': profile_data.get('minor', ''),
                'courses': profile_data.get('courses', ''),
                'interests': profile_data.get('interests', '')
            }
            return JsonResponse({'success': True, 'data': response_data})
        else:
            default_data = {
                'full_name': user_full_name,
                'title': '',
                'school': '',
                'year_level': '',  # Changed from 'year'
                'location': '',
                'graduation_yr': '',  # Changed from 'graduation_year'
                'about': '',
                'specialization': '',
                'major': '',
                'minor': '',
                'courses': '',
                'interests': ''
            }
            return JsonResponse({'success': True, 'data': default_data})
            
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        user_full_name = request.user.get_full_name() or request.user.username
        default_data = {
            'full_name': user_full_name,
            'title': '',
            'school': '',
            'year_level': '',  # Changed from 'year'
            'location': '',
            'graduation_yr': '',  # Changed from 'graduation_year'
            'about': '',
            'specialization': '',
            'major': '',
            'minor': '',
            'courses': '',
            'interests': ''
        }
        return JsonResponse({'success': True, 'data': default_data})




def get_user_projects_django(user):
    """
    Get ONLY the projects that belong to the current user
    Returns empty queryset if user has no projects
    """
    try:
        # Try to get user profile
        user_profile = UserProfile.objects.get(user=user)
        
        # Return ONLY projects where author is this user's profile
        return Project.objects.filter(author=user_profile).order_by('-created_at')
        
    except UserProfile.DoesNotExist:
        # If no user profile exists, user has no projects
        pass
    
    # Return EMPTY queryset - user has no projects
    return Project.objects.none()

# PROJECT-RELATED VIEWS - ADD THESE FUNCTIONS

@login_required
def add_project(request):
    """
    Handle project creation - both form display and submission
    """
    if request.method == 'POST':
        try:
            # Get or create user profile
            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': request.user.get_full_name() or request.user.username,
                    'bio': '',
                    'school': '',
                    'major': ''
                }
            )
            
            # Create the project WITH SCREENSHOT HANDLING
            project = Project(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                tech_used=request.POST.get('tech_used', ''),
                github_url=request.POST.get('github_url', ''),
                live_demo=request.POST.get('live_demo', ''),
                category=request.POST.get('category', 'other'),
                status='completed',
                author=user_profile,
                screenshot=request.FILES.get('screenshot')  # ADD THIS LINE
            )
            project.save()
            
            # Also save to Supabase for consistency
            try:
                supabase_data = {
                    'user_id': str(request.user.id),
                    'title': project.title,
                    'description': project.description,
                    'tech_used': project.tech_used,
                    'github_url': project.github_url,
                    'live_demo': project.live_demo,
                    'category': project.category,
                    'status': 'completed',
                    'created_at': project.created_at.isoformat()
                }
                
                supabase_client.table('projects_project') \
                    .insert([supabase_data]) \
                    .execute()
            except Exception as e:
                print(f"Warning: Could not sync to Supabase: {e}")
            
            return redirect('user_profile')
            
        except Exception as e:
            print(f"Error creating project: {e}")
            # Return form with error
            return render(request, 'projects/project_form.html', {
                'error': 'There was an error creating your project. Please try again.'
            })
    
    # GET request - show the form
    return render(request, 'projects/project_form.html')

@login_required
def view_project(request, project_id):
    """
    Display a specific project
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user owns this project or it's public
    if project.author.user != request.user:
        # For now, allow viewing any project
        # You might want to add privacy controls later
        pass
    
    # FIXED: Changed from project_detail.html to view_project.html
    return render(request, 'projects/view_project.html', {'project': project})

@login_required
def edit_project(request, project_id):
    """
    Handle project editing
    """
    try:
        # FIX: Use get_or_create to handle missing UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        project = get_object_or_404(Project, id=project_id, author=user_profile)
        
        if request.method == 'POST':
            try:
                project.title = request.POST.get('title', project.title)
                project.description = request.POST.get('description', project.description)
                project.tech_used = request.POST.get('tech_used', project.tech_used)
                project.github_url = request.POST.get('github_url', project.github_url)
                project.live_demo = request.POST.get('live_demo', project.live_demo)
                project.category = request.POST.get('category', project.category)
                
                # Handle new screenshot upload (only if file is provided)
                if 'screenshot' in request.FILES and request.FILES['screenshot']:
                    project.screenshot = request.FILES['screenshot']
                
                project.save()
                
                # Redirect back to previous page using next parameter
                next_url = request.POST.get('next') or 'user_profile'
                return redirect(next_url)
                
            except Exception as e:
                print(f"Error updating project: {e}")
                return render(request, 'projects/project_form.html', {
                    'project': project,
                    'editing': True,  # ADD THIS LINE
                    'error': 'There was an error updating your project.'
                })
        
        # GET request - show edit form WITH BOTH project AND editing
        context = {
            'project': project,
            'editing': True  # THIS IS CRITICAL - WAS MISSING!
        }
        return render(request, 'projects/project_form.html', context)
        
    except Exception as e:
        print(f"Error accessing project: {str(e)}")
        return redirect('user_profile')

@login_required
def delete_project(request, project_id):
    """
    Handle project deletion
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user owns this project
    if project.author.user != request.user:
        return redirect('user_profile')
    
    if request.method == 'POST':
        project.delete()
        return redirect('user_profile')
    
    return render(request, 'projects/confirm_delete.html', {'project': project})

# EXISTING VIEWS - KEEP THESE

def landing_page(request):
    return render(request, 'dashboard/landing_page.html')

def gallery(request):
    """Project gallery view - publicly accessible (shows ALL projects)"""
    print(f"Gallery accessed - User: {request.user}, Auth: {request.user.is_authenticated}")
    projects = Project.objects.all().select_related('author__user').order_by('-created_at')
    return render(request, "projects/gallery.html", {"projects": projects})


@login_required
def dashboard(request):
    # Get ONLY the user's own projects
    user_projects = get_user_projects_django(request.user)
    
    total_projects = user_projects.count()
    recent_submissions = user_projects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Calculate technologies from user's projects only
    all_techs = []
    for project in user_projects:
        if project.tech_used:
            techs = [tech.strip() for tech in project.tech_used.replace(',', ' ').split() if tech.strip()]
            all_techs.extend(techs)
    total_technologies = len(set(all_techs)) if all_techs else 0
    
    # Calculate categories from user's projects only
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
    
    # Get user's most viewed and latest project (will be None if no projects)
    most_viewed_project = user_projects.order_by('-views').first()
    latest_project = user_projects.first()
    
    # Calculate engagement based on user's own projects
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
        'user_projects': user_projects,  # This will be EMPTY if user has no projects
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


@login_required
def debug_user_data(request):
    """Simple view to see what user data exists"""
    user = request.user
    
    print(f"=== DEBUG USER DATA ===")
    print(f"User ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"First Name: {user.first_name}")
    print(f"Last Name: {user.last_name}")
    print(f"Full Name: {user.get_full_name()}")
    
    # Try to get Django UserProfile (from accounts app)
    try:
        from accounts.models import UserProfile
        profile = UserProfile.objects.get(user=user)
        print(f"Django UserProfile found:")
        print(f"  - Student ID: {profile.student_id}")
        print(f"  - Department: {profile.department}")
        print(f"  - Year Level: {profile.year_level}")
    except ImportError:
        print("Could not import UserProfile from accounts")
    except UserProfile.DoesNotExist:
        print(f"No Django UserProfile found")
    
    # Also check Supabase data
    try:
        supabase_data = get_user_profile_from_supabase(user.id)
        print(f"Supabase data: {supabase_data}")
    except Exception as e:
        print(f"Supabase error: {e}")
    
    # Show this in browser too
    context = {
        'debug_user': user,
        'debug_profile': None,
        'supabase_data': None,
    }
    
    try:
        from accounts.models import UserProfile
        context['debug_profile'] = UserProfile.objects.get(user=user)
    except:
        pass
    
    try:
        context['supabase_data'] = get_user_profile_from_supabase(user.id)
    except:
        pass
    
    return render(request, 'dashboard/debug_user_data.html', context)

def get_user_profile_from_supabase(user_id):
    try:
        print(f"🔥 get_user_profile_from_supabase called for user_id: {user_id}")
        
        response = supabase_client.table('accounts_userprofile') \
            .select('*') \
            .eq('user_id', str(user_id)) \
            .execute()
        
        print(f"🔥 Supabase response status: Success")
        print(f"🔥 Data found: {bool(response.data)}")
        print(f"🔥 Number of records: {len(response.data) if response.data else 0}")
        
        if response.data and len(response.data) > 0:
            profile_data = response.data[0]
            print(f"🔥 Raw Supabase profile data: {profile_data}")
            
            # Print all columns to see what we actually have
            print(f"🔥 Available columns in Supabase:")
            for key, value in profile_data.items():
                print(f"🔥   '{key}': '{value}'")
            
            return profile_data
        
        print(f"🔥 No profile found in Supabase for user {user_id}")
        return None
        
    except Exception as e:
        print(f"🔥 Error fetching user profile from Supabase: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_user_projects_supabase(user_id):
    try:
        response = supabase_client.table('projects_project') \
            .select('*') \
            .eq('user_id', str(user_id)) \
            .order('created_at', desc=True) \
            .execute()
        
        return response.data
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return None
@login_required
def save_profile_to_supabase(request):
    if request.method == 'POST':
        try:
            user_id = str(request.user.id)
            user = request.user
            user_full_name = user.get_full_name() or user.username

            # FIX: Use correct database column names
            profile_data = {
                'user_id': user_id,
                'full_name': request.POST.get('full_name', user_full_name),  # Changed from 'name'
                'title': request.POST.get('title', ''),
                'school': request.POST.get('school', ''),
                'year_level': request.POST.get('year_level', ''),  # Changed from 'year'
                'location': request.POST.get('location', ''),
                'graduation_yr': request.POST.get('graduation_yr', ''),  # Changed from 'graduation_year'
                'about': request.POST.get('about', ''),
                'specialization': request.POST.get('specialization', ''),
                'major': request.POST.get('major', ''),
                'minor': request.POST.get('minor', ''),
                'courses': request.POST.get('courses', ''),
                'interests': request.POST.get('interests', ''),
                'updated_at': timezone.now().isoformat()
            }

            existing_profile = supabase_client.table('accounts_userprofile') \
                .select('user_id') \
                .eq('user_id', user_id) \
                .execute()

            if existing_profile.data and len(existing_profile.data) > 0:
                response = supabase_client.table('accounts_userprofile') \
                    .update(profile_data) \
                    .eq('user_id', user_id) \
                    .execute()
            else:
                profile_data['created_at'] = timezone.now().isoformat()
                response = supabase_client.table('accounts_userprofile') \
                    .insert([profile_data]) \
                    .execute()

            return JsonResponse({'success': True, 'message': 'Profile saved successfully!'})

        except Exception as e:
            print(f"Error saving profile: {e}")
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def save_project_to_supabase(request):
    if request.method == 'POST':
        try:
            user_id = str(request.user.id)
            project_data = {
                'user_id': user_id,
                'title': request.POST.get('projectName', ''),
                'description': request.POST.get('projectDescription', ''),
                'tech_used': request.POST.get('projectLanguages', ''),
                'github_url': request.POST.get('projectLink', ''),
                'live_demo': request.POST.get('projectLink', ''),
                'category': 'Software',
                'status': 'completed',
                'created_at': timezone.now().isoformat()
            }
            
            response = supabase_client.table('projects_project') \
                .insert([project_data]) \
                .execute()
            
            return JsonResponse({'success': True, 'message': 'Project saved successfully!'})
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return JsonResponse({'success': False, 'message': 'Error saving project.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def get_supabase_profile_data(request):
    try:
        user_id = str(request.user.id)
        user = request.user
        profile_data = get_user_profile_from_supabase(user_id)
        
        user_full_name = user.get_full_name() or user.username
        
        if profile_data:
            profile_data['full_name'] = profile_data.get('full_name') or user_full_name
            return JsonResponse({'success': True, 'data': profile_data})
        else:
            default_data = {
                'full_name': user_full_name,
                'title': '',
                'school': '',
                'year_level': '',
                'location': '',
                'graduation_year': '',
                'about': '',
                'specialization': '',
                'major': '',
                'minor': '',
                'courses': '',
                'interests': ''
            }
            return JsonResponse({'success': True, 'data': default_data})
            
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        user_full_name = request.user.get_full_name() or request.user.username
        default_data = {
            'full_name': user_full_name,
            'title': '',
            'school': '',
            'year_level': '',
            'location': '',
            'graduation_year': '',
            'about': '',
            'specialization': '',
            'major': '',
            'minor': '',
            'courses': '',
            'interests': ''
        }
        return JsonResponse({'success': True, 'data': default_data})

@login_required
def get_supabase_profile_data(request):
    try:
        user_id = str(request.user.id)
        user = request.user
        profile_data = get_user_profile_from_supabase(user_id)
        
        user_full_name = user.get_full_name() or user.username
        
        if profile_data:
            # Use correct field mapping
            response_data = {
                'full_name': profile_data.get('full_name') or user_full_name,
                'title': profile_data.get('title', ''),
                'school': profile_data.get('school', ''),
                'year_level': profile_data.get('year_level', ''),  # Correct field name
                'location': profile_data.get('location', ''),
                'graduation_yr': profile_data.get('graduation_yr', ''),  # Correct field name
                'about': profile_data.get('about', ''),
                'specialization': profile_data.get('specialization', ''),
                'major': profile_data.get('major', ''),
                'minor': profile_data.get('minor', ''),
                'courses': profile_data.get('courses', ''),
                'interests': profile_data.get('interests', '')
            }
            return JsonResponse({'success': True, 'data': response_data})
        else:
            default_data = {
                'full_name': user_full_name,
                'title': '',
                'school': '',
                'year_level': '',  # Changed from 'year'
                'location': '',
                'graduation_yr': '',  # Changed from 'graduation_year'
                'about': '',
                'specialization': '',
                'major': '',
                'minor': '',
                'courses': '',
                'interests': ''
            }
            return JsonResponse({'success': True, 'data': default_data})
            
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        user_full_name = request.user.get_full_name() or request.user.username
        default_data = {
            'full_name': user_full_name,
            'title': '',
            'school': '',
            'year_level': '',  # Changed from 'year'
            'location': '',
            'graduation_yr': '',  # Changed from 'graduation_year'
            'about': '',
            'specialization': '',
            'major': '',
            'minor': '',
            'courses': '',
            'interests': ''
        }
        return JsonResponse({'success': True, 'data': default_data})




def get_user_projects_django(user):
    """
    Get ONLY the projects that belong to the current user
    Returns empty queryset if user has no projects
    """
    try:
        # Try to get user profile
        user_profile = UserProfile.objects.get(user=user)
        
        # Return ONLY projects where author is this user's profile
        return Project.objects.filter(author=user_profile).order_by('-created_at')
        
    except UserProfile.DoesNotExist:
        # If no user profile exists, user has no projects
        pass
    
    # Return EMPTY queryset - user has no projects
    return Project.objects.none()

# PROJECT-RELATED VIEWS - ADD THESE FUNCTIONS

@login_required
def add_project(request):
    """
    Handle project creation - both form display and submission
    """
    if request.method == 'POST':
        try:
            # Get or create user profile
            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': request.user.get_full_name() or request.user.username,
                    'bio': '',
                    'school': '',
                    'major': ''
                }
            )
            
            # Create the project WITH SCREENSHOT HANDLING
            project = Project(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                tech_used=request.POST.get('tech_used', ''),
                github_url=request.POST.get('github_url', ''),
                live_demo=request.POST.get('live_demo', ''),
                category=request.POST.get('category', 'other'),
                status='completed',
                author=user_profile,
                screenshot=request.FILES.get('screenshot')  # ADD THIS LINE
            )
            project.save()
            
            # Also save to Supabase for consistency
            try:
                supabase_data = {
                    'user_id': str(request.user.id),
                    'title': project.title,
                    'description': project.description,
                    'tech_used': project.tech_used,
                    'github_url': project.github_url,
                    'live_demo': project.live_demo,
                    'category': project.category,
                    'status': 'completed',
                    'created_at': project.created_at.isoformat()
                }
                
                supabase_client.table('projects_project') \
                    .insert([supabase_data]) \
                    .execute()
            except Exception as e:
                print(f"Warning: Could not sync to Supabase: {e}")
            
            return redirect('user_profile')
            
        except Exception as e:
            print(f"Error creating project: {e}")
            # Return form with error
            return render(request, 'projects/project_form.html', {
                'error': 'There was an error creating your project. Please try again.'
            })
    
    # GET request - show the form
    return render(request, 'projects/project_form.html')

@login_required
def view_project(request, project_id):
    """
    Display a specific project
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user owns this project or it's public
    if project.author.user != request.user:
        # For now, allow viewing any project
        # You might want to add privacy controls later
        pass
    
    # FIXED: Changed from project_detail.html to view_project.html
    return render(request, 'projects/view_project.html', {'project': project})

@login_required
def edit_project(request, project_id):
    """
    Handle project editing
    """
    try:
        # FIX: Use get_or_create to handle missing UserProfile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        project = get_object_or_404(Project, id=project_id, author=user_profile)
        
        if request.method == 'POST':
            try:
                project.title = request.POST.get('title', project.title)
                project.description = request.POST.get('description', project.description)
                project.tech_used = request.POST.get('tech_used', project.tech_used)
                project.github_url = request.POST.get('github_url', project.github_url)
                project.live_demo = request.POST.get('live_demo', project.live_demo)
                project.category = request.POST.get('category', project.category)
                
                # Handle new screenshot upload (only if file is provided)
                if 'screenshot' in request.FILES and request.FILES['screenshot']:
                    project.screenshot = request.FILES['screenshot']
                
                project.save()
                
                # Redirect back to previous page using next parameter
                next_url = request.POST.get('next') or 'user_profile'
                return redirect(next_url)
                
            except Exception as e:
                print(f"Error updating project: {e}")
                return render(request, 'projects/project_form.html', {
                    'project': project,
                    'editing': True,  # ADD THIS LINE
                    'error': 'There was an error updating your project.'
                })
        
        # GET request - show edit form WITH BOTH project AND editing
        context = {
            'project': project,
            'editing': True  # THIS IS CRITICAL - WAS MISSING!
        }
        return render(request, 'projects/project_form.html', context)
        
    except Exception as e:
        print(f"Error accessing project: {str(e)}")
        return redirect('user_profile')

@login_required
def delete_project(request, project_id):
    """
    Handle project deletion
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Check if user owns this project
    if project.author.user != request.user:
        return redirect('user_profile')
    
    if request.method == 'POST':
        project.delete()
        return redirect('user_profile')
    
    return render(request, 'projects/confirm_delete.html', {'project': project})

# EXISTING VIEWS - KEEP THESE

def landing_page(request):
    return render(request, 'dashboard/landing_page.html')

def gallery(request):
    """Project gallery view - publicly accessible (shows ALL projects)"""
    print(f"Gallery accessed - User: {request.user}, Auth: {request.user.is_authenticated}")
    projects = Project.objects.all().select_related('author__user').order_by('-created_at')
    return render(request, "projects/gallery.html", {"projects": projects})


@login_required
def dashboard(request):
    # Get ONLY the user's own projects
    user_projects = get_user_projects_django(request.user)
    
    total_projects = user_projects.count()
    recent_submissions = user_projects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Calculate technologies from user's projects only
    all_techs = []
    for project in user_projects:
        if project.tech_used:
            techs = [tech.strip() for tech in project.tech_used.replace(',', ' ').split() if tech.strip()]
            all_techs.extend(techs)
    total_technologies = len(set(all_techs)) if all_techs else 0
    
    # Calculate categories from user's projects only
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
    
    # Get user's most viewed and latest project (will be None if no projects)
    most_viewed_project = user_projects.order_by('-views').first()
    latest_project = user_projects.first()
    
    # Calculate engagement based on user's own projects
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
    
    # --- FETCH ACTIVE ANNOUNCEMENTS ---
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'user_projects': user_projects,  # This will be EMPTY if user has no projects
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
        'announcements': announcements, # <--- Added to context
    }
    
    return render(request, 'dashboard/dashboard.html', context)