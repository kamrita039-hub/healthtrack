from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FamilyMember, HealthRecord


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class FamilyMemberForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = FamilyMember
        fields = ['name', 'relation', 'date_of_birth', 'blood_group', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class HealthRecordForm(forms.ModelForm):
    diagnosis_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    recovery_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = HealthRecord
        fields = [
            'title', 'category', 'severity', 'status',
            'diagnosis_date', 'recovery_date',
            'doctor_name', 'hospital',
            'description', 'medications'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'medications': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g. Metformin 500mg, Aspirin 75mg'}),
        }
