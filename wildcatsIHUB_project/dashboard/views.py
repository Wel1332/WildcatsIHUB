from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

def get_user_profile_from_supabase(user_id):
    try:
        response = supabase_client.table('accounts_userprofile') \
            .select('*') \
            .eq('user_id', str(user_id)) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching user profile: {e}")
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

            profile_data = {
                'user_id': user_id,
                'full_name': request.POST.get('name', user_full_name),
                'title': request.POST.get('title', ''),
                'school': request.POST.get('school', ''),
                'year_level': request.POST.get('year', ''),
                'location': request.POST.get('location', ''),
                'graduation_year': request.POST.get('graduation', ''),
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
def user_profile(request):
    try:
        user_profile_data = get_user_profile_from_supabase(request.user.id)
        user = request.user
        
        if not user_profile_data:
            user_full_name = user.get_full_name() or user.username
            user_profile_data = {
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
        
        django_projects = get_user_projects_django(request.user)
        
        context = {
            'projects': django_projects,
            'user_profile_data': user_profile_data
        }
        return render(request, 'dashboard/userProfile.html', context)
        
    except Exception as e:
        print(f"Error in user_profile view: {e}")
        projects = Project.objects.all()
        user = request.user
        user_full_name = user.get_full_name() or user.username
        default_profile = {
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
        context = {
            'projects': projects,
            'user_profile_data': default_profile
        }
        return render(request, 'dashboard/userProfile.html', context)

def get_user_projects_django(user):
    user_projects = Project.objects.none()
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        
        if Project.objects.filter(author=user_profile).exists():
            user_projects = Project.objects.filter(author=user_profile).order_by('-created_at')
        elif Project.objects.filter(created_by=user_profile).exists():
            user_projects = Project.objects.filter(created_by=user_profile).order_by('-created_at')
        elif Project.objects.filter(user=user).exists():
            user_projects = Project.objects.filter(user=user).order_by('-created_at')
        elif Project.objects.filter(owner=user).exists():
            user_projects = Project.objects.filter(owner=user).order_by('-created_at')
        else:
            user_projects = Project.objects.all().order_by('-created_at')
            
    except UserProfile.DoesNotExist:
        if Project.objects.filter(user=user).exists():
            user_projects = Project.objects.filter(user=user).order_by('-created_at')
        elif Project.objects.filter(owner=user).exists():
            user_projects = Project.objects.filter(owner=user).order_by('-created_at')
        else:
            user_projects = Project.objects.all().order_by('-created_at')
    
    return user_projects

def landing_page(request):
    return render(request, 'dashboard/landing_page.html')

@login_required
def dashboard(request):
    user_projects = get_user_projects_django(request.user)
    
    total_projects = user_projects.count()
    recent_submissions = user_projects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    all_techs = []
    for project in user_projects:
        if project.tech_used:
            techs = [tech.strip() for tech in project.tech_used.replace(',', ' ').split() if tech.strip()]
            all_techs.extend(techs)
    total_technologies = len(set(all_techs)) if all_techs else 0
    
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
    
    most_viewed_project = user_projects.order_by('-views').first()
    latest_project = user_projects.first()
    
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