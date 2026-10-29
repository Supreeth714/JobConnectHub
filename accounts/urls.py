from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('candidate/profile/', views.candidate_profile_view, name='candidate_profile'),
    path('recruiter/profile/', views.recruiter_profile_view, name='recruiter_profile'),
]
