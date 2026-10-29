from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('mine/', views.my_applications, name='my_applications'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('<int:app_id>/status/', views.update_status, name='update_status'),
    path('<int:app_id>/email/', views.email_candidate, name='email_candidate'),
]
