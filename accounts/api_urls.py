from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api_views

urlpatterns = [
    path('auth/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('accounts/me/', api_views.MeAPIView.as_view(), name='api_me'),
    path('accounts/profile/', api_views.ProfileAPIView.as_view(), name='api_profile'),
]
