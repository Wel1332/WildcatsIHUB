from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('submit/', views.submit_project, name='submit_project'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('projects/', views.view_project, name='view_project'),
    path('project/<int:project_id>/', views.view_project, name='view_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('approvals/', views.approval_system, name='approvals'),
    path('project-tracking/', views.project_tracking, name='project_tracking'),
    path('submissions/', views.submissions, name='submissions'),
    path('gallery/', views.project_gallery, name='gallery'),
    path('profile/', views.profile_settings, name='profile'),
     path('home/', views.project_gallery, name='home'),
]