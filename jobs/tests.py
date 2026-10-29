from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Company, RecruiterProfile
from jobs.forms import JobForm
from jobs.models import Job

User = get_user_model()


class JobCreateTests(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1',
            email='rec@example.com',
            password='testpass123',
            role='recruiter',
        )
        self.company = Company.objects.create(
            name='Test Company',
            description='A test company.',
            location='Test City',
            website='https://example.com',
        )
        RecruiterProfile.objects.create(user=self.recruiter, company=self.company)

    def test_job_form_save_commit_false_does_not_require_company(self):
        form_data = {
            'title': 'Test Job',
            'description': 'Job description',
            'requirements': 'Job requirements',
            'location': 'Remote',
            'job_type': 'full_time',
            'salary_min': '50000',
            'salary_max': '70000',
            'experience_required': '2',
            'is_active': True,
            'skills_text': 'Python, Django',
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
        job = form.save(commit=False)
        self.assertIsNone(job.pk)
        self.assertIsNone(job.company_id)
        self.assertEqual(job.title, 'Test Job')

    def test_job_create_view_posts_job_with_company_and_skills(self):
        self.client.login(username='recruiter1', password='testpass123')
        response = self.client.post(
            reverse('job_create'),
            data={
                'title': 'Posted Job',
                'description': 'A posted job description',
                'requirements': 'Requirements here',
                'location': 'Remote',
                'job_type': 'full_time',
                'salary_min': '60000',
                'salary_max': '80000',
                'experience_required': '3',
                'is_active': 'on',
                'skills_text': 'Python, Django',
            },
        )
        self.assertRedirects(response, reverse('job_detail', args=[1]))
        job = Job.objects.get(title='Posted Job')
        self.assertEqual(job.company, self.company)
        self.assertEqual(job.posted_by, self.recruiter)
        self.assertQuerysetEqual(
            job.skills.order_by('name').values_list('name', flat=True),
            ['Django', 'Python'],
            ordered=True,
        )
