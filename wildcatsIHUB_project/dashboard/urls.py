from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-profile/', views.user_profile, name='user_profile'),
    
    # Supabase integration endpoints
    path('user-profile/save/', views.save_profile_to_supabase, name='save_profile'),
    path('user-profile/save-project/', views.save_project_to_supabase, name='save_project'),
    path('user-profile/data/', views.get_supabase_profile_data, name='get_profile_data'),
]