from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CandidateProfile, RecruiterProfile, Company, Skill


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')


class CandidateProfileForm(forms.ModelForm):
    skills_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React'}),
        help_text='Comma-separated skills',
    )

    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'headline', 'bio', 'experience_years', 'location',
                  'resume', 'photo', 'linkedin', 'github']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        skills_text = self.cleaned_data.get('skills_text', '')
        if skills_text:
            names = [s.strip() for s in skills_text.split(',') if s.strip()]
            skill_objs = []
            for name in names:
                s, _ = Skill.objects.get_or_create(name=name)
                skill_objs.append(s)
            instance.skills.set(skill_objs)
        return instance


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'location', 'website', 'logo']


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['full_name', 'position', 'photo']
