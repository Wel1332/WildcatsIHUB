from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('submit/', views.submit_project, name='submit_project'),
]