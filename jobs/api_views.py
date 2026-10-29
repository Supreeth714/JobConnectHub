from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer
from accounts.permissions import IsRecruiter, IsOwnerRecruiter


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True).select_related('company').prefetch_related('skills')
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'location', 'company']
    search_fields = ['title', 'description', 'skills__name', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsRecruiter()]
        return [permissions.IsAuthenticated(), IsRecruiter(), IsOwnerRecruiter()]
