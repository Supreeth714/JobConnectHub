from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job
from .forms import JobForm
from accounts.models import RecruiterProfile, CandidateProfile, Skill
from applications.models import Application


def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('company')
    q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    skill = request.GET.get('skill', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(skills__name__icontains=q)).distinct()
    if location:
        jobs = jobs.filter(location__icontains=location)
    if skill:
        jobs = jobs.filter(skills__name__icontains=skill).distinct()
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs, 'q': q, 'location': location, 'skill': skill, 'job_type': job_type,
        'job_types': Job.JOB_TYPES,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    if request.user.is_authenticated and request.user.is_candidate():
        already_applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})


@login_required
def job_create(request):
    if not request.user.is_recruiter():
        messages.error(request, 'Only recruiters can post jobs.')
        return redirect('job_list')
    profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
    if not profile.company:
        messages.warning(request, 'Please complete your company profile first.')
        return redirect('recruiter_profile')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = profile.company
            job.posted_by = request.user
            job.save()
            form.save_m2m()
            # save skills via custom logic
            text = form.cleaned_data.get('skills_text', '')
            if text:
                objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in text.split(',') if n.strip()]
                job.skills.set(objs)
            messages.success(request, 'Job posted!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'mode': 'Create'})


@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated.')
            return redirect('job_detail', pk=job.pk)
    else:
        initial = {'skills_text': ', '.join(job.skills.values_list('name', flat=True))}
        form = JobForm(instance=job, initial=initial)
    return render(request, 'jobs/job_form.html', {'form': form, 'mode': 'Update'})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
        return redirect('recruiter_dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
