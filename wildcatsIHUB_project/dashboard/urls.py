from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-profile/', views.user_profile, name='user_profile'),
    
]