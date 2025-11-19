from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth.models import User
from projects.models import Project 
from accounts.models import UserProfile 
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AdminUserForm, AdminProfileForm, UserManagementForm, UserProfileEditForm, ProjectForm

def is_admin(user):
    return user.is_active and user.is_staff

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)                     
def admin_dashboard(request):
    total_users = UserProfile.objects.count()
    approved_projects_count = Project.objects.filter(status='Approved').count()
    ongoing_projects_count = Project.objects.filter(status='Active').count()
    recent_projects = Project.objects.all().order_by('-created_at')[:5] 
    for project in recent_projects:
        project.badge_class = 'active' if project.status == 'Active' else (
            'completed' if project.status == 'Completed' else 'pending'
        )

    context = {
        'total_users': total_users,
        'approved_projects_count': approved_projects_count,
        'ongoing_projects_count': ongoing_projects_count,
        'projects': recent_projects, 
        'admin_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, "adminpanel/admin_dashboard.html", context)

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)
def approvals(request):
    pending_projects = Project.objects.filter(status='Pending').order_by('created_at')
    
    context = {
        "pending_projects": pending_projects,
    }
    return render(request, "adminpanel/approvals.html", context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
@require_POST # Security: Only allow POST requests (form submissions)
def approve_reject_project(request, pk):
    """Handles updating a project's status to Approved or Rejected."""
    
    # 1. Retrieve the project instance
    project = get_object_or_404(Project, pk=pk)
    
    # 2. Determine the action (Approve or Reject) from the hidden form field
    action = request.POST.get('action') 
    
    if action == 'Approve':
        project.status = 'Approved'
        message = f'Project "{project.title}" has been successfully approved.'
    elif action == 'Reject':
        project.status = 'Rejected'
        message = f'Project "{project.title}" has been rejected.'
    else:
        messages.error(request, "Invalid action requested.")
        return redirect('approvals')

    # 3. Save the new status to the database
    project.save()
    
    messages.success(request, message)
    
    # 4. Redirect back to the pending approvals list
    return redirect('approvals')

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)
def gallery(request):
    projects = Project.objects.all().order_by('-created_at')
    
    context = {
        "projects": projects,
    }
    return render(request, "adminpanel/gallery.html", context)

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)
def submissions(request):
    all_submissions = Project.objects.all().select_related('author').order_by('-created_at')
    submission_stats = {
        "total": all_submissions.count(),
        "approved": Project.objects.filter(status='Approved').count(),
        "rejected": Project.objects.filter(status='Rejected').count(),
        "pending": Project.objects.filter(status='Pending').count(),
    }
    
    context = {
        "submissions": all_submissions,
        "stats": submission_stats,
    }
    return render(request, "adminpanel/submissions.html", context)

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)
def user_management(request):
    users = UserProfile.objects.all().order_by('user__username')
    
    context = {
        "users": users,
    }
    return render(request, "adminpanel/user_management.html", context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
def user_detail(request, pk):
    """Displays the read-only details of a specific user."""
    # Retrieve the User instance and ensure the related UserProfile exists
    user_instance = get_object_or_404(User, pk=pk)
    # The profile should exist due to our get_or_create fix
    profile_instance = user_instance.userprofile 
    
    context = {
        'user_to_view': user_instance,
        'profile': profile_instance,
    }
    return render(request, 'adminpanel/user_detail.html', context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
@transaction.atomic
def user_edit(request, pk):
    # 1. Retrieve instances (User and related UserProfile)
    user_instance = get_object_or_404(User, pk=pk)
    profile_instance, created = UserProfile.objects.get_or_create(user=user_instance)
    
    if request.method == 'POST':
        # Bind POST data to both forms
        user_form = UserManagementForm(request.POST, instance=user_instance)
        profile_form = UserProfileEditForm(request.POST, instance=profile_instance)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'User {user_instance.username} updated successfully!')
            return redirect('user_management') # Redirect back to the user list
        else:
            messages.error(request, 'Please correct the errors below.')
            
    else:
        # GET request: load forms with existing data
        user_form = UserManagementForm(instance=user_instance)
        profile_form = UserProfileEditForm(instance=profile_instance)
        
    context = {
        'user_to_edit': user_instance,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'adminpanel/user_edit.html', context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
def user_delete(request, pk):
    """Handles the user deletion confirmation and process."""
    user_instance = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        # Safety check: Prevent accidental deletion of superusers
        if user_instance.is_superuser:
            messages.error(request, "Cannot delete superuser accounts.")
            return redirect('user_management')
            
        user_instance.delete()
        messages.success(request, f'User {user_instance.username} successfully deleted.')
        return redirect('user_management')

    # GET request: Show confirmation page
    context = {
        'user_to_delete': user_instance,
    }
    return render(request, 'adminpanel/user_delete_confirm.html', context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
def project_tracking(request):
    projects = Project.objects.all().select_related('author').order_by('-created_at')
    
    context = {
        "projects": projects
    }
    return render(request, "adminpanel/project_tracking.html", context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
def project_detail(request, pk):
    """Displays the read-only details of a specific project."""
    # Fetch the project instance, and pre-fetch the author/user data
    project_instance = get_object_or_404(
        Project.objects.select_related('author__user'), 
        pk=pk
    )
    
    # Apply badge class logic for consistent display
    project_instance.badge_class = 'active' if project_instance.status == 'Active' else (
        'completed' if project_instance.status == 'Completed' else 'pending'
    )
    
    context = {
        'project': project_instance,
    }
    return render(request, 'adminpanel/project_detail.html', context)

@login_required(login_url='/accounts/login/')
@user_passes_test(is_admin)
def project_edit(request, pk):
    """Handles editing a specific project."""
    project_instance = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        # Handle file uploads (screenshot) and post data
        form = ProjectForm(request.POST, request.FILES, instance=project_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project_instance.title}" updated successfully.')
            return redirect('project_detail', pk=pk) # Redirect to the detail view
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = ProjectForm(instance=project_instance)

    context = {
        'form': form,
        'project': project_instance,
    }
    return render(request, 'adminpanel/project_edit.html', context)

@login_required(login_url='/accounts/login/') 
@user_passes_test(is_admin)
def admin_profile(request):
    # FIX: Use get_or_create to ensure the profile exists
    # If the profile doesn't exist, Django will create a default one now.
    profile_instance, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # FIX: Pass request.FILES to the forms that handle files (AdminProfileForm)
        user_form = AdminUserForm(request.POST, instance=request.user)
        profile_form = AdminProfileForm(request.POST, request.FILES, instance=profile_instance)

        if user_form.is_valid() and profile_form.is_valid():
            # Save data to both models
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('admin_profile') # Redirect back to the profile page

        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        # 3. For GET request, instantiate forms with current data
        user_form = AdminUserForm(instance=request.user)
        profile_form = AdminProfileForm(request.POST, request.FILES, instance=profile_instance)

    context = {
        "user": request.user,
        "user_form": user_form,
        "profile_form": profile_form
    }
    return render(request, "adminpanel/admin_profile.html", context)