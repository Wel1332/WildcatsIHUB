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
import time
import jwt 

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
        email = data.get('email', '').lower().strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required'})
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            redirect_to = "http://127.0.0.1:8000/accounts/reset-password/"
            
            print(f"🔧 DEBUG: Sending reset email to {email}")
            print(f"🔧 DEBUG: Redirect URL: {redirect_to}")
            
            result = supabase.auth.reset_password_for_email(
                email,
                {
                    "redirect_to": redirect_to
                }
            )
            
            if hasattr(result, 'error') and result.error:
                error_msg = str(result.error)
                print(f"❌ Supabase error: {error_msg}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Failed to send reset email. Please try again.'
                })
            
            print(f"✅ Password reset email sent to: {email}")
            return JsonResponse({
                'success': True, 
                'message': 'Password reset link sent! Check your email inbox AND spam folder.'
            })
            
        except Exception as email_error:
            print(f"❌ Email sending error: {email_error}")
            return JsonResponse({
                'success': False, 
                'error': 'Email service temporarily unavailable. Please try again.'
            })
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return JsonResponse({
            'success': False, 
            'error': 'System error. Please try again.'
        })
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required'})
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **CHANGE THIS TO POINT TO THE CONFIRM PAGE, NOT DONE PAGE**
            redirect_to = "http://127.0.0.1:8000/accounts/reset-password/"  # This should be the page that shows the form
            
            print(f"🔧 DEBUG: Sending reset email to {email}")
            print(f"🔧 DEBUG: Redirect URL: {redirect_to}")
            
            result = supabase.auth.reset_password_for_email(
                email,
                {
                    "redirect_to": redirect_to
                }
            )
            
            if hasattr(result, 'error') and result.error:
                error_msg = str(result.error)
                print(f"❌ Supabase error: {error_msg}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Failed to send reset email. Please try again.'
                })
            
            print(f"✅ Password reset email sent to: {email}")
            return JsonResponse({
                'success': True, 
                'message': 'Password reset link sent! Check your email inbox AND spam folder.'
            })
            
        except Exception as email_error:
            print(f"❌ Email sending error: {email_error}")
            return JsonResponse({
                'success': False, 
                'error': 'Email service temporarily unavailable. Please try again.'
            })
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return JsonResponse({
            'success': False, 
            'error': 'System error. Please try again.'
        })
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required'})
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **UPDATE THIS TO MATCH YOUR SUPABASE SETTINGS**
            redirect_to = "http://127.0.0.1:8000/accounts/reset-password/"
            
            print(f"🔧 DEBUG: Sending reset email to {email}")
            print(f"🔧 DEBUG: Redirect URL: {redirect_to}")
            
            result = supabase.auth.reset_password_for_email(
                email,
                {
                    "redirect_to": redirect_to
                }
            )
            
            if hasattr(result, 'error') and result.error:
                error_msg = str(result.error)
                print(f"❌ Supabase error: {error_msg}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Failed to send reset email. Please try again.'
                })
            
            print(f"✅ Password reset email sent to: {email}")
            return JsonResponse({
                'success': True, 
                'message': 'Password reset link sent! Check your email inbox AND spam folder.'
            })
            
        except Exception as email_error:
            print(f"❌ Email sending error: {email_error}")
            return JsonResponse({
                'success': False, 
                'error': 'Email service temporarily unavailable. Please try again.'
            })
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return JsonResponse({
            'success': False, 
            'error': 'System error. Please try again.'
        })
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required'})
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **FIX: Use EXACT URL format that Supabase expects**
            redirect_to = "http://127.0.0.1:8000/accounts/reset-password/"  # NO TRAILING SLASH
            
            print(f"🔧 DEBUG: Sending reset email to {email}")
            print(f"🔧 DEBUG: Redirect URL: {redirect_to}")
            
            # **FIX: Use the CORRECT Supabase method**
            result = supabase.auth.reset_password_for_email(
                email,
                {
                    "redirect_to": redirect_to
                }
            )
            
            # **FIX: Check for errors properly**
            if hasattr(result, 'error') and result.error:
                error_msg = str(result.error)
                print(f"❌ Supabase error: {error_msg}")
                return JsonResponse({
                    'success': False, 
                    'error': 'Failed to send reset email. Please try again.'
                })
            
            print(f"✅ Password reset email sent to: {email}")
            return JsonResponse({
                'success': True, 
                'message': 'Password reset link sent! Check your email inbox AND spam folder.'
            })
            
        except Exception as email_error:
            print(f"❌ Email sending error: {email_error}")
            return JsonResponse({
                'success': False, 
                'error': 'Email service temporarily unavailable. Please try again.'
            })
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return JsonResponse({
            'success': False, 
            'error': 'System error. Please try again.'
        })

def reset_password_confirm(request):
    """Handle password reset confirmation - CAPTURE THE TOKEN"""
    print(f"🔧 DEBUG: Reset password page accessed")
    print(f"🔧 DEBUG: Full URL: {request.build_absolute_uri()}")
    
    # Check if there's a hash in the URL that contains the token
    full_url = request.build_absolute_uri()
    if 'access_token=' in full_url:
        # Extract token from the full URL (JavaScript will handle this properly)
        print("✅ DEBUG: URL contains access_token (will be handled by JavaScript)")
    
    return render(request, 'accounts/reset_password_confirm.html')

def reset_password_done(request):
    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        try:
            # **METHOD 1: Try using the service role key to update password directly**
            print("🔄 DEBUG: Using Service Role Key approach")
            
            # Create Supabase client with service role key
            admin_supabase = create_client(
                os.getenv('SUPABASE_URL'),
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpenNhenh0aHZ2YXZoZGJvd3ppIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDMyNTY5NCwiZXhwIjoyMDc1OTAxNjk0fQ.2jXmNmae6-k3pv5Ja-WlFjnyvh_T_z9BQa4-SnV29GM"
            )
            
            # Extract user email from the JWT token
            import jwt
            try:
                # Decode the JWT token to get user info
                decoded = jwt.decode(token, options={"verify_signature": False})
                user_email = decoded.get('email')
                user_id = decoded.get('sub')
                
                print(f"🔧 DEBUG: Extracted from token - Email: {user_email}, User ID: {user_id}")
                
                if user_id:
                    # **METHOD 1A: Update user by ID using admin API**
                    print("🔄 DEBUG: METHOD 1A - Updating user by ID")
                    admin_response = admin_supabase.auth.admin.update_user_by_id(
                        user_id,
                        {"password": new_password}
                    )
                    
                    if hasattr(admin_response, 'error') and admin_response.error:
                        error_msg = str(admin_response.error)
                        print(f"🔧 DEBUG: Update by ID failed: {error_msg}")
                        
                        # **METHOD 1B: Try updating user by email**
                        print("🔄 DEBUG: METHOD 1B - Updating user by email")
                        if user_email:
                            admin_response = admin_supabase.auth.admin.update_user_by_email(
                                user_email,
                                {"password": new_password}
                            )
                            
                            if hasattr(admin_response, 'error') and admin_response.error:
                                error_msg = str(admin_response.error)
                                print(f"🔧 DEBUG: Update by email failed: {error_msg}")
                                raise Exception(f"Admin update failed: {error_msg}")
                    
                    print("✅ DEBUG: Password reset successful via Admin API")
                    messages.success(request, 'Password reset successfully! You can now login with your new password.')
                    return redirect('login')
                
            except Exception as admin_error:
                print(f"🔧 DEBUG: Admin API approach failed: {admin_error}")
                
                # **METHOD 2: Fallback to regular verify_otp**
                print("🔄 DEBUG: METHOD 2 - Trying verify_otp as fallback")
                
                regular_supabase = create_client(
                    os.getenv('SUPABASE_URL'),
                    os.getenv('SUPABASE_KEY')
                )
                
                result = regular_supabase.auth.verify_otp({
                    "token_hash": token,
                    "type": "recovery",
                    "password": new_password
                })
                
                if hasattr(result, 'error') and result.error:
                    error_msg = str(result.error)
                    print(f"🔧 DEBUG: OTP verification failed: {error_msg}")
                    raise Exception(f"All methods failed: {error_msg}")
                
                print("✅ DEBUG: Password reset successful via OTP")
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                return redirect('login')
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            error_msg = str(e)
            if "invalid" in error_msg.lower() or "expired" in error_msg.lower():
                messages.error(request, 'Invalid or expired reset link. Please request a new password reset.')
            elif "jwt" in error_msg.lower():
                messages.error(request, 'Invalid reset token format.')
            else:
                messages.error(request, f'Password reset failed: {error_msg}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    return redirect('reset_password_confirm')



    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **CORRECT APPROACH: Use the Supabase admin API or direct method**
            print("🔄 DEBUG: Using direct Supabase approach")
            
            # Method 1: Try to use the token as a recovery token
            # For Supabase, the token from email should work with verify_otp
            # But we need to make sure it's the correct format
            
            # Clean the token (remove any URL parameters if present)
            clean_token = token.split('&')[0] if '&' in token else token
            clean_token = clean_token.split('?')[0] if '?' in clean_token else clean_token
            
            print(f"🔧 DEBUG: Cleaned token: {clean_token[:50]}...")
            
            # Try verify_otp with the cleaned token
            result = supabase.auth.verify_otp({
                "token_hash": clean_token,
                "type": "recovery",
                "password": new_password
            })
            
            if hasattr(result, 'error') and result.error:
                error_msg = str(result.error)
                print(f"🔧 DEBUG: OTP verification failed: {error_msg}")
                
                # If OTP fails, try using the admin API approach
                print("🔄 DEBUG: Trying admin API approach...")
                
                # Extract user ID from the JWT token
                import jwt
                try:
                    # Decode the JWT token to get user info (without verification for now)
                    decoded = jwt.decode(clean_token, options={"verify_signature": False})
                    user_id = decoded.get('sub')
                    print(f"🔧 DEBUG: Extracted user ID from token: {user_id}")
                    
                    if user_id:
                        # Use Supabase admin API to update password
                        # This requires the service_role key instead of anon key
                        admin_supabase = create_client(
                            os.getenv('SUPABASE_URL'),
                            os.getenv('SUPABASE_SERVICE_KEY')  # You need to set this in your env
                        )
                        
                        # Update user password using admin API
                        admin_response = admin_supabase.auth.admin.update_user_by_id(
                            user_id,
                            {"password": new_password}
                        )
                        
                        if hasattr(admin_response, 'error') and admin_response.error:
                            admin_error = str(admin_response.error)
                            print(f"🔧 DEBUG: Admin API failed: {admin_error}")
                            raise Exception(f"Password reset failed: {admin_error}")
                        
                        print("✅ DEBUG: Password reset successful via Admin API")
                        messages.success(request, 'Password reset successfully! You can now login with your new password.')
                        return redirect('login')
                    else:
                        raise Exception("Could not extract user ID from token")
                        
                except Exception as admin_error:
                    print(f"🔧 DEBUG: Admin approach failed: {admin_error}")
                    raise Exception("All password reset methods failed")
            
            print("✅ DEBUG: Password reset successful via OTP")
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('login')
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            error_msg = str(e)
            if "invalid" in error_msg.lower() or "expired" in error_msg.lower():
                messages.error(request, 'Invalid or expired reset link. Please request a new password reset.')
            else:
                messages.error(request, f'Password reset failed: {error_msg}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    return redirect('reset_password_confirm')


    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            print("🔄 DEBUG: Using JWT token for password reset")
            
            # **METHOD 1: Try to create a session first using the token**
            print("🔄 DEBUG: METHOD 1 - Creating session with token")
            
            # The token from the email is a JWT access_token that can be used to get a session
            try:
                # Get the user using the token
                user_response = supabase.auth.get_user(token)
                
                if hasattr(user_response, 'error') and user_response.error:
                    print(f"🔧 DEBUG: Get user failed: {user_response.error}")
                    raise Exception(f"Authentication failed: {user_response.error}")
                
                print("✅ DEBUG: User authenticated successfully")
                
                # Now update the password
                update_response = supabase.auth.update_user({
                    "password": new_password
                })
                
                if hasattr(update_response, 'error') and update_response.error:
                    error_msg = str(update_response.error)
                    print(f"🔧 DEBUG: Password update failed: {error_msg}")
                    raise Exception(f"Password update failed: {error_msg}")
                
                print(f"✅ DEBUG: Password reset successful via METHOD 1")
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                return redirect('login')
                
            except Exception as method1_error:
                print(f"🔧 DEBUG: METHOD 1 failed: {method1_error}")
                
                # **METHOD 2: Try using the token as a recovery token with verify_otp**
                print("🔄 DEBUG: METHOD 2 - Using token as recovery token")
                try:
                    # Extract just the JWT part (before any additional parameters)
                    jwt_token = token.split('&')[0] if '&' in token else token
                    
                    verify_result = supabase.auth.verify_otp({
                        "token_hash": jwt_token,
                        "type": "recovery",
                        "password": new_password
                    })
                    
                    if hasattr(verify_result, 'error') and verify_result.error:
                        error_msg = str(verify_result.error)
                        print(f"🔧 DEBUG: OTP verification failed: {error_msg}")
                        raise Exception(f"OTP verification failed: {error_msg}")
                    
                    print(f"✅ DEBUG: Password reset successful via METHOD 2")
                    messages.success(request, 'Password reset successfully! You can now login with your new password.')
                    return redirect('login')
                    
                except Exception as method2_error:
                    print(f"🔧 DEBUG: METHOD 2 failed: {method2_error}")
                    
                    # **METHOD 3: Try the exchange_code_for_session approach**
                    print("🔄 DEBUG: METHOD 3 - Exchange code for session")
                    try:
                        exchange_response = supabase.auth.exchange_code_for_session({
                            "auth_code": token
                        })
                        
                        if hasattr(exchange_response, 'error') and exchange_response.error:
                            error_msg = str(exchange_response.error)
                            print(f"🔧 DEBUG: Session exchange failed: {error_msg}")
                            raise Exception(f"Session exchange failed: {error_msg}")
                        
                        # Now update password with active session
                        update_response = supabase.auth.update_user({
                            "password": new_password
                        })
                        
                        if hasattr(update_response, 'error') and update_response.error:
                            error_msg = str(update_response.error)
                            print(f"🔧 DEBUG: Password update failed: {error_msg}")
                            raise Exception(f"Password update failed: {error_msg}")
                        
                        print(f"✅ DEBUG: Password reset successful via METHOD 3")
                        messages.success(request, 'Password reset successfully! You can now login with your new password.')
                        return redirect('login')
                        
                    except Exception as method3_error:
                        print(f"🔧 DEBUG: METHOD 3 failed: {method3_error}")
                        
                        # **METHOD 4: Manual approach - create client with token**
                        print("🔄 DEBUG: METHOD 4 - Manual client creation")
                        try:
                            # Create a new client with the token
                            auth_supabase = create_client(
                                os.getenv('SUPABASE_URL'),
                                os.getenv('SUPABASE_KEY')
                            )
                            
                            # Manually set the access token
                            auth_supabase.auth.set_session({
                                "access_token": token,
                                "refresh_token": token,  # Use same as fallback
                                "token_type": "bearer",
                                "expires_in": 3600,
                                "expires_at": time.time() + 3600,
                                "user": None
                            })
                            
                            # Now update password
                            update_response = auth_supabase.auth.update_user({
                                "password": new_password
                            })
                            
                            if hasattr(update_response, 'error') and update_response.error:
                                error_msg = str(update_response.error)
                                print(f"🔧 DEBUG: Password update failed: {error_msg}")
                                raise Exception(f"Password update failed: {error_msg}")
                            
                            print(f"✅ DEBUG: Password reset successful via METHOD 4")
                            messages.success(request, 'Password reset successfully! You can now login with your new password.')
                            return redirect('login')
                            
                        except Exception as method4_error:
                            print(f"🔧 DEBUG: METHOD 4 failed: {method4_error}")
                            raise Exception("All password reset methods failed")
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    # If not POST, redirect to the form page
    return redirect('reset_password_confirm')

    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **CORRECT METHOD: Use the JWT token directly with Supabase**
            print("🔄 DEBUG: Using JWT token for password reset")
            
            # For JWT tokens from email, we need to use a different approach
            # The token contains both access_token and refresh_token information
            
            # Try to update the password using the token
            update_response = supabase.auth.update_user({
                "password": new_password
            })
            
            if hasattr(update_response, 'error') and update_response.error:
                error_msg = str(update_response.error)
                print(f"🔧 DEBUG: Password update error: {error_msg}")
                
                # If that fails, try using the token as a session
                print("🔄 DEBUG: Trying alternative method...")
                
                # Create a new client instance and set the token
                supabase_with_token = create_client(
                    os.getenv('SUPABASE_URL'),
                    os.getenv('SUPABASE_KEY'),
                    {
                        'access_token': token,
                        'refresh_token': token  # Use same token as fallback
                    }
                )
                
                # Try to update password with the authenticated client
                update_response2 = supabase_with_token.auth.update_user({
                    "password": new_password
                })
                
                if hasattr(update_response2, 'error') and update_response2.error:
                    error_msg = str(update_response2.error)
                    print(f"🔧 DEBUG: Alternative method also failed: {error_msg}")
                    raise Exception(f"Password reset failed: {error_msg}")
                
                print(f"✅ DEBUG: Password reset successful via alternative method")
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                return redirect('login')
            
            print(f"✅ DEBUG: Password reset successful")
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('login')
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    # If not POST, redirect to the form page
    return redirect('reset_password_confirm')
    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **USE THE CORRECT METHOD FOR JWT TOKENS**
            # For JWT tokens received via email, we need to use them differently
            
            # Method: Update user with the token as authorization
            update_response = supabase.auth.update_user(
                {"password": new_password},
                # Pass the token as the authorization header
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if hasattr(update_response, 'error') and update_response.error:
                error_msg = str(update_response.error)
                print(f"🔧 DEBUG: Password update error: {error_msg}")
                
                # Fallback: Try the OTP method
                print("🔄 DEBUG: Trying OTP method as fallback...")
                verify_result = supabase.auth.verify_otp({
                    "token_hash": token,
                    "type": "recovery", 
                    "password": new_password
                })
                
                if hasattr(verify_result, 'error') and verify_result.error:
                    error_msg = str(verify_result.error)
                    print(f"🔧 DEBUG: OTP fallback also failed: {error_msg}")
                    
                    if "invalid" in error_msg.lower() or "expired" in error_msg.lower():
                        messages.error(request, 'Invalid or expired reset link. Please request a new password reset.')
                    else:
                        messages.error(request, f'Password reset failed: {error_msg}')
                    
                    return render(request, 'accounts/reset_password_confirm.html')
                
                print(f"✅ DEBUG: Password reset successful via OTP fallback")
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                return redirect('login')
            
            print(f"✅ DEBUG: Password reset successful via direct update")
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('login')
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    # If not POST, redirect to the form page
    return redirect('reset_password_confirm')

    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        print(f"🔧 DEBUG: Token length: {len(token) if token else 0}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **METHOD 1: Try using the token directly with update_user (for JWT tokens)**
            print("🔄 DEBUG: Trying METHOD 1 - update_user with JWT token")
            
            # First, let's try to use the token to create a session
            try:
                # Set the session using the JWT token
                session_response = supabase.auth.set_session(token)
                
                if hasattr(session_response, 'error') and session_response.error:
                    print(f"🔧 DEBUG: set_session failed: {session_response.error}")
                    raise Exception("Session creation failed")
                
                # Now update the password with the active session
                update_response = supabase.auth.update_user({
                    "password": new_password
                })
                
                if hasattr(update_response, 'error') and update_response.error:
                    error_msg = str(update_response.error)
                    print(f"🔧 DEBUG: Password update error: {error_msg}")
                    raise Exception(f"Password update failed: {error_msg}")
                
                print(f"✅ DEBUG: Password reset successful via METHOD 1")
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                
                # Sign out after password reset
                supabase.auth.sign_out()
                    
                return redirect('login')
                
            except Exception as method1_error:
                print(f"🔧 DEBUG: METHOD 1 failed: {method1_error}")
                
                # **METHOD 2: Try verify_otp with the token as token_hash**
                print("🔄 DEBUG: Trying METHOD 2 - verify_otp")
                try:
                    verify_result = supabase.auth.verify_otp({
                        "token_hash": token,
                        "type": "recovery",
                        "password": new_password
                    })
                    
                    if hasattr(verify_result, 'error') and verify_result.error:
                        error_msg = str(verify_result.error)
                        print(f"🔧 DEBUG: OTP verification error: {error_msg}")
                        raise Exception(f"OTP verification failed: {error_msg}")
                    
                    print(f"✅ DEBUG: Password reset successful via METHOD 2")
                    messages.success(request, 'Password reset successfully! You can now login with your new password.')
                    return redirect('login')
                    
                except Exception as method2_error:
                    print(f"🔧 DEBUG: METHOD 2 failed: {method2_error}")
                    
                    # **METHOD 3: Try the exchange_code_for_session approach**
                    print("🔄 DEBUG: Trying METHOD 3 - exchange_code_for_session")
                    try:
                        # For JWT tokens, we might need to exchange them
                        exchange_response = supabase.auth.exchange_code_for_session({
                            "auth_code": token
                        })
                        
                        if hasattr(exchange_response, 'error') and exchange_response.error:
                            error_msg = str(exchange_response.error)
                            print(f"🔧 DEBUG: Session exchange error: {error_msg}")
                            raise Exception(f"Session exchange failed: {error_msg}")
                        
                        # Now update password
                        update_response = supabase.auth.update_user({
                            "password": new_password
                        })
                        
                        if hasattr(update_response, 'error') and update_response.error:
                            error_msg = str(update_response.error)
                            print(f"🔧 DEBUG: Password update error: {error_msg}")
                            raise Exception(f"Password update failed: {error_msg}")
                        
                        print(f"✅ DEBUG: Password reset successful via METHOD 3")
                        messages.success(request, 'Password reset successfully! You can now login with your new password.')
                        
                        # Sign out after password reset
                        supabase.auth.sign_out()
                            
                        return redirect('login')
                        
                    except Exception as method3_error:
                        print(f"🔧 DEBUG: METHOD 3 failed: {method3_error}")
                        raise Exception("All password reset methods failed")
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    # If not POST, show the form again
    return render(request, 'accounts/reset_password_confirm.html')


    """Handle the actual password reset"""
    if request.method == 'POST':
        token = request.POST.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        print(f"🔧 DEBUG: Password reset attempt - token: {token}")
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        if len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/reset_password_confirm.html')
        
        supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        try:
            # **CORRECT METHOD: Use verify_otp with password for recovery**
            verify_result = supabase.auth.verify_otp({
                "token_hash": token,
                "type": "recovery",
                "password": new_password  # This sets the new password directly
            })
            
            if hasattr(verify_result, 'error') and verify_result.error:
                error_msg = str(verify_result.error)
                print(f"🔧 DEBUG: OTP verification error: {error_msg}")
                
                if "invalid" in error_msg.lower() or "expired" in error_msg.lower():
                    messages.error(request, 'Invalid or expired reset link. Please request a new password reset.')
                else:
                    messages.error(request, f'Password reset failed: {error_msg}')
                
                return render(request, 'accounts/reset_password_confirm.html')
            
            print(f"✅ DEBUG: Password reset successful via OTP verification")
            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('login')
            
        except Exception as e:
            print(f"🔧 DEBUG: Password reset exception: {e}")
            messages.error(request, f'Password reset failed: {str(e)}')
            return render(request, 'accounts/reset_password_confirm.html')
    
    # If not POST, show the form again
    return render(request, 'accounts/reset_password_confirm.html')


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

                if django_user.is_staff or django_user.is_superuser:
                    # Redirect to your custom admin dashboard view
                    return redirect('admin_dashboard') 
                else:
                    # Regular user redirects to the home view
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