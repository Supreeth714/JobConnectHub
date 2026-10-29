from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, CandidateProfile, RecruiterProfile, Company, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'candidate'),
        )
        if user.role == 'candidate':
            CandidateProfile.objects.create(user=user)
        else:
            RecruiterProfile.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = CandidateProfile
        fields = ['id', 'user', 'full_name', 'headline', 'bio', 'experience_years',
                  'location', 'skills', 'skill_names', 'resume', 'photo',
                  'linkedin', 'github']

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if skill_names is not None:
            objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in skill_names if n.strip()]
            instance.skills.set(objs)
        return instance


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False
    )

    class Meta:
        model = RecruiterProfile
        fields = ['id', 'user', 'full_name', 'company', 'company_id', 'position', 'photo']
