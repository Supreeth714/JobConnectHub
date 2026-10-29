from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Application
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    if not request.user.is_candidate():
        messages.error(request, 'Only candidates can apply.')
        return redirect('job_list')
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.info(request, 'You already applied to this job.')
        return redirect('job_detail', pk=job.pk)
    if request.method == 'POST':
        cover = request.POST.get('cover_letter', '')
        Application.objects.create(job=job, candidate=request.user, cover_letter=cover)
        messages.success(request, 'Application submitted!')
        return redirect('my_applications')
    return render(request, 'applications/apply.html', {'job': job})


@login_required
def my_applications(request):
    if not request.user.is_candidate():
        return redirect('dashboard')
    apps_qs = Application.objects.filter(candidate=request.user).select_related('job', 'job__company')
    return render(request, 'applications/my_applications.html', {'applications': apps_qs})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, pk=job_id, posted_by=request.user)
    apps_qs = Application.objects.filter(job=job).select_related('candidate', 'candidate__candidate_profile')
    skill_filter = request.GET.get('skill', '').strip()
    if skill_filter:
        apps_qs = apps_qs.filter(candidate__candidate_profile__skills__name__icontains=skill_filter).distinct()
    return render(request, 'applications/job_applicants.html', {
        'job': job, 'applications': apps_qs, 'skill_filter': skill_filter,
    })


@login_required
def update_status(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__posted_by=request.user)
    if request.method == 'POST':
        status_val = request.POST.get('status')
        if status_val in dict(Application.STATUS_CHOICES):
            app.status = status_val
            app.save()
            messages.success(request, f'Status updated to {app.get_status_display()}.')
    return redirect('job_applicants', job_id=app.job.id)


@login_required
def email_candidate(request, app_id):
    app = get_object_or_404(Application, pk=app_id, job__posted_by=request.user)
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()
        if subject and body:
            send_mail(
                subject, body, settings.DEFAULT_FROM_EMAIL,
                [app.candidate.email], fail_silently=False,
            )
            messages.success(request, f'Email sent to {app.candidate.email}.')
            return redirect('job_applicants', job_id=app.job.id)
        messages.error(request, 'Subject and body are required.')
    return render(request, 'applications/email_candidate.html', {'application': app})
