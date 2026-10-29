from django import forms
from .models import Job
from accounts.models import Skill


class JobForm(forms.ModelForm):
    skills_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, REST'}),
        help_text='Comma-separated required skills',
    )

    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'job_type',
                  'salary_min', 'salary_max', 'experience_required', 'is_active']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            text = self.cleaned_data.get('skills_text', '')
            if text:
                objs = [Skill.objects.get_or_create(name=n.strip())[0] for n in text.split(',') if n.strip()]
                instance.skills.set(objs)
        return instance
