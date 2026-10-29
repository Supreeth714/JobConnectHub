from django.urls import path
from . import api_views

urlpatterns = [
    path('applications/apply/<int:job_id>/', api_views.ApplyJobAPIView.as_view(), name='api_apply'),
    path('applications/mine/', api_views.MyApplicationsAPIView.as_view(), name='api_my_apps'),
    path('applications/job/<int:job_id>/', api_views.JobApplicantsAPIView.as_view(), name='api_job_applicants'),
    path('applications/<int:pk>/status/', api_views.UpdateApplicationStatusAPIView.as_view(), name='api_update_status'),
    path('applications/<int:pk>/email/', api_views.EmailCandidateAPIView.as_view(), name='api_email_candidate'),
]
