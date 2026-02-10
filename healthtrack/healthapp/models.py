from django.db import models
from django.contrib.auth.models import User


class FamilyMember(models.Model):
    RELATION_CHOICES = [
        ('self', 'Myself'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('spouse', 'Spouse'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
        ('uncle', 'Uncle'),
        ('aunt', 'Aunt'),
        ('other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('unknown', 'Unknown'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='unknown')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_relation_display()})"

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class HealthRecord(models.Model):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active / Ongoing'),
        ('recovered', 'Recovered'),
        ('chronic', 'Chronic (Managed)'),
        ('monitoring', 'Under Monitoring'),
    ]

    CATEGORY_CHOICES = [
        ('disease', 'Disease'),
        ('surgery', 'Surgery'),
        ('allergy', 'Allergy'),
        ('mental_health', 'Mental Health'),
        ('dental', 'Dental'),
        ('vision', 'Vision / Eye'),
        ('heart', 'Heart / Cardiovascular'),
        ('diabetes', 'Diabetes'),
        ('cancer', 'Cancer'),
        ('injury', 'Injury / Accident'),
        ('vaccination', 'Vaccination'),
        ('other', 'Other'),
    ]

    family_member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='health_records')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='mild')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    diagnosis_date = models.DateField()
    recovery_date = models.DateField(null=True, blank=True)
    doctor_name = models.CharField(max_length=100, blank=True)
    hospital = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    medications = models.TextField(blank=True, help_text='List medications separated by commas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.family_member.name}"

    class Meta:
        ordering = ['-diagnosis_date']
