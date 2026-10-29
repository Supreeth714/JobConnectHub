from rest_framework import serializers
from .models import Application
from accounts.serializers import UserSerializer, CandidateProfileSerializer
from accounts.models import CandidateProfile


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    candidate_profile = serializers.SerializerMethodField()
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'company_name', 'candidate', 'candidate_profile',
                  'cover_letter', 'status', 'applied_at', 'updated_at']
        read_only_fields = ['status', 'applied_at', 'updated_at', 'candidate']

    def get_candidate_profile(self, obj):
        try:
            return CandidateProfileSerializer(obj.candidate.candidate_profile).data
        except CandidateProfile.DoesNotExist:
            return None
