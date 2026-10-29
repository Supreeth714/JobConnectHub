from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CANDIDATE = 'candidate'
    ROLE_RECRUITER = 'recruiter'
    ROLE_CHOICES = [
        (ROLE_CANDIDATE, 'Candidate'),
        (ROLE_RECRUITER, 'Recruiter'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CANDIDATE)
    email = models.EmailField(unique=True)

    def is_candidate(self):
        return self.role == self.ROLE_CANDIDATE

    def is_recruiter(self):
        return self.role == self.ROLE_RECRUITER

    def __str__(self):
        return f"{self.username} ({self.role})"


class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=120, blank=True)
    headline = models.CharField(max_length=200, blank=True, help_text="e.g. Senior Frontend Engineer")
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=120, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='candidates')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"Candidate: {self.user.username}"


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    full_name = models.CharField(max_length=120, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='recruiters')
    position = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"Recruiter: {self.user.username}"
