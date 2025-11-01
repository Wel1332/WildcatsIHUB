from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password_confirm, name='reset_password_confirm'),  
    path('reset-password-done/', views.reset_password_done, name='reset_password_done'),
]