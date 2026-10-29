from rest_framework import serializers
from .models import Job
from accounts.serializers import SkillSerializer, CompanySerializer
from accounts.models import Skill


class JobSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    company = CompanySerializer(read_only=True)
    posted_by_username = serializers.CharField(source='posted_by.username', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'requirements', 'location', 'job_type',
                  'salary_min', 'salary_max', 'experience_required', 'skills', 'skill_names',
                  'company', 'posted_by_username', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['company', 'created_at', 'updated_at']

    def create(self, validated_data):
        skill_names = validated_data.pop('skill_names', [])
        request = self.context['request']
        company = request.user.recruiter_profile.company
        job = Job.objects.create(company=company, posted_by=request.user, **validated_data)
        if skill_names:
            objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in skill_names if n.strip()]
            job.skills.set(objs)
        return job

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if skill_names is not None:
            objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in skill_names if n.strip()]
            instance.skills.set(objs)
        return instance
