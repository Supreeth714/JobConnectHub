from django.urls import path, include

urlpatterns = [
    path('', include('accounts.api_urls')),
    path('', include('jobs.api_urls')),
    path('', include('applications.api_urls')),
]
