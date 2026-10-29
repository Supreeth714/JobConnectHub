from django.contrib import admin
from .models import User, Skill, CandidateProfile, RecruiterProfile, Company

admin.site.site_header = "JobConnectHub Admin"
admin.site.site_title = "JobConnectHub"
admin.site.index_title = "Dashboard"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(Skill)
admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Company)
