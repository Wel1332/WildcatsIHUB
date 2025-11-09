from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('approvals/', views.approvals, name='approvals'),
    path('project-tracking/', views.project_tracking, name='project_tracking'),
    path('submissions/', views.submissions, name='submissions'),
    path('profile/', views.admin_profile, name='admin_profile'),  # NOT 'profile'
]