from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('submit/', views.submit_project, name='submit_project'),
]
