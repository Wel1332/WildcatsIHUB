from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('user_management/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_management/view/<int:pk>/', views.user_detail, name='user_detail'),
    path('user_management/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('approvals/', views.approvals, name='approvals'),
    path('approvals/action/<int:pk>/', views.approve_reject_project, name='approve_reject_project'),
    path('project-tracking/', views.project_tracking, name='project_tracking'),
    path('project-tracking/view/<int:pk>/', views.project_detail, name='project_detail'),
    path('project-tracking/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('submissions/', views.submissions, name='submissions'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('gallery/', views.gallery, name='gallery'),
    path('projects/bulk-action/', views.bulk_project_action, name='bulk_project_action'),
]