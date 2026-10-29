from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer, UserSerializer,
    CandidateProfileSerializer, RecruiterProfileSerializer,
)
from .models import CandidateProfile, RecruiterProfile


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ProfileAPIView(APIView):
    """Return / update current user's profile (candidate or recruiter)."""

    def get(self, request):
        if request.user.is_candidate():
            p, _ = CandidateProfile.objects.get_or_create(user=request.user)
            return Response(CandidateProfileSerializer(p).data)
        p, _ = RecruiterProfile.objects.get_or_create(user=request.user)
        return Response(RecruiterProfileSerializer(p).data)

    def put(self, request):
        if request.user.is_candidate():
            p, _ = CandidateProfile.objects.get_or_create(user=request.user)
            ser = CandidateProfileSerializer(p, data=request.data, partial=True)
        else:
            p, _ = RecruiterProfile.objects.get_or_create(user=request.user)
            ser = RecruiterProfileSerializer(p, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
