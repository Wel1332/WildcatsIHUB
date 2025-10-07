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


]