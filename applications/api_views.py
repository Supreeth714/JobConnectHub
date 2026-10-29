from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job
from accounts.permissions import IsCandidate, IsRecruiter


class ApplyJobAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def post(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id, is_active=True)
        if Application.objects.filter(job=job, candidate=request.user).exists():
            return Response({'detail': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)
        app = Application.objects.create(
            job=job, candidate=request.user,
            cover_letter=request.data.get('cover_letter', ''),
        )
        return Response(ApplicationSerializer(app).data, status=status.HTTP_201_CREATED)


class MyApplicationsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user)


class JobApplicantsAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        qs = Application.objects.filter(job_id=job_id, job__posted_by=self.request.user)
        skill = self.request.query_params.get('skill')
        if skill:
            qs = qs.filter(candidate__candidate_profile__skills__name__icontains=skill).distinct()
        return qs


class UpdateApplicationStatusAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def patch(self, request, pk):
        app = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
        new_status = request.data.get('status')
        if new_status not in dict(Application.STATUS_CHOICES):
            return Response({'detail': 'Invalid status'}, status=400)
        app.status = new_status
        app.save()
        return Response(ApplicationSerializer(app).data)


class EmailCandidateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRecruiter]

    def post(self, request, pk):
        app = get_object_or_404(Application, pk=pk, job__posted_by=request.user)
        subject = request.data.get('subject', '').strip()
        body = request.data.get('body', '').strip()
        if not subject or not body:
            return Response({'detail': 'subject and body required'}, status=400)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [app.candidate.email])
        return Response({'detail': f'Email sent to {app.candidate.email}'})
