from django.contrib import admin
from .models import FamilyMember, HealthRecord

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'relation', 'user', 'blood_group', 'date_of_birth']
    list_filter = ['relation', 'blood_group']
    search_fields = ['name', 'user__username']

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'family_member', 'category', 'severity', 'status', 'diagnosis_date']
    list_filter = ['category', 'severity', 'status']
    search_fields = ['title', 'family_member__name']
