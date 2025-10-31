from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from supabase import create_client
import os
import json
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import StudentLoginForm

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
        
            return render(request, 'accounts/signup.html', {
                'success_message': '✅ Verification email resent! Please check your inbox and spam folder.',
                'resend_email': email
            })
        except Exception as e:
            return render(request, 'accounts/signup.html', {
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
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        year_level = request.POST.get('year_level')
        
        try:
            # Initialize Supabase client
            supabase = create_client(
                os.getenv('SUPABASE_URL'),
                os.getenv('SUPABASE_KEY')
            )
            
            # Check if email already exists in Django
            if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                error_msg = 'Email already registered! Please use a different email or login.'
                return render(request, 'accounts/signup.html', {'error': error_msg})
            
            # Check if student ID already exists
            if UserProfile.objects.filter(student_id=student_id).exists():
                error_msg = 'Student ID already exists! Please use a different Student ID.'
                return render(request, 'accounts/signup.html', {'error': error_msg})
            
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
                return render(request, 'accounts/signup.html', {
                    'success_message': success_message
                })
            else:
                error_msg = 'Failed to create authentication account. Please try again.'
                return render(request, 'accounts/signup.html', {'error': error_msg})
                
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
            
            return render(request, 'accounts/signup.html', {'error': error_msg})
            
        except Exception as e:
            try:
                User.objects.filter(username=email).delete()
            except:
                pass
                
            error_msg = f'Error creating account: {str(e)}'
            return render(request, 'accounts/signup.html', {'error': error_msg})
    
    return render(request, 'accounts/signup.html')