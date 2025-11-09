from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('submit/', views.submit_project, name='submit_project'),
    path('project/<int:project_id>/', views.view_project, name='view_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('gallery/', views.gallery, name='gallery'),
    path('profile/', views.user_profile, name='profile'),
]