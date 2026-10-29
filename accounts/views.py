from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, CandidateProfileForm, RecruiterProfileForm, CompanyForm
from .models import CandidateProfile, RecruiterProfile, Company


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'candidate':
                CandidateProfile.objects.create(user=user)
            else:
                RecruiterProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to JobConnectHub!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required
def dashboard_redirect(request):
    if request.user.is_recruiter():
        return redirect('recruiter_dashboard')
    return redirect('candidate_dashboard')


@login_required
def candidate_dashboard(request):
    if not request.user.is_candidate():
        return redirect('dashboard')
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    from jobs.models import Job
    from applications.models import Application
    jobs_qs = Job.objects.filter(is_active=True).order_by('-created_at')[:5]
    apps_qs = Application.objects.filter(candidate=request.user).order_by('-applied_at')[:5]
    return render(request, 'accounts/candidate_dashboard.html', {
        'profile': profile, 'jobs': jobs_qs, 'applications': apps_qs,
    })


@login_required
def recruiter_dashboard(request):
    if not request.user.is_recruiter():
        return redirect('dashboard')
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
    from jobs.models import Job
    jobs_qs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'accounts/recruiter_dashboard.html', {
        'profile': profile, 'jobs': jobs_qs,
    })


@login_required
def candidate_profile_view(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('candidate_profile')
    else:
        initial = {'skills_text': ', '.join(profile.skills.values_list('name', flat=True))}
        form = CandidateProfileForm(instance=profile, initial=initial)
    return render(request, 'accounts/candidate_profile.html', {'form': form, 'profile': profile})


@login_required
def recruiter_profile_view(request):
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
    company = profile.company
    if request.method == 'POST':
        pform = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
        cform = CompanyForm(request.POST, request.FILES, instance=company) if company else CompanyForm(request.POST, request.FILES)
        if pform.is_valid() and cform.is_valid():
            comp = cform.save()
            rp = pform.save(commit=False)
            rp.company = comp
            rp.save()
            messages.success(request, 'Profile updated.')
            return redirect('recruiter_profile')
    else:
        pform = RecruiterProfileForm(instance=profile)
        cform = CompanyForm(instance=company) if company else CompanyForm()
    return render(request, 'accounts/recruiter_profile.html', {'pform': pform, 'cform': cform})
