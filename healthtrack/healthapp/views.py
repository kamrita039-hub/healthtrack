from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count
from .models import FamilyMember, HealthRecord
from .forms import RegisterForm, FamilyMemberForm, HealthRecordForm


# ─── AUTH VIEWS ───────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ─── DASHBOARD ────────────────────────────────────────────────

@login_required
def dashboard(request):
    members = FamilyMember.objects.filter(user=request.user).annotate(
        record_count=Count('health_records')
    )
    total_records = HealthRecord.objects.filter(family_member__user=request.user).count()
    active_records = HealthRecord.objects.filter(
        family_member__user=request.user, status='active'
    ).count()
    chronic_records = HealthRecord.objects.filter(
        family_member__user=request.user, status='chronic'
    ).count()
    recent_records = HealthRecord.objects.filter(
        family_member__user=request.user
    ).select_related('family_member').order_by('-created_at')[:5]

    context = {
        'members': members,
        'total_records': total_records,
        'active_records': active_records,
        'chronic_records': chronic_records,
        'recent_records': recent_records,
        'member_count': members.count(),
    }
    return render(request, 'dashboard.html', context)


# ─── FAMILY MEMBER VIEWS ──────────────────────────────────────

@login_required
def member_list(request):
    members = FamilyMember.objects.filter(user=request.user).annotate(
        record_count=Count('health_records')
    )
    return render(request, 'members/list.html', {'members': members})


@login_required
def member_add(request):
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, f'{member.name} added to your family!')
            return redirect('member_detail', pk=member.pk)
    else:
        form = FamilyMemberForm()
    return render(request, 'members/form.html', {'form': form, 'action': 'Add'})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, user=request.user)
    records = member.health_records.all()
    active = records.filter(status='active')
    chronic = records.filter(status='chronic')
    recovered = records.filter(status='recovered')
    return render(request, 'members/detail.html', {
        'member': member,
        'records': records,
        'active': active,
        'chronic': chronic,
        'recovered': recovered,
    })


@login_required
def member_edit(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'{member.name} updated successfully!')
            return redirect('member_detail', pk=pk)
    else:
        form = FamilyMemberForm(instance=member)
    return render(request, 'members/form.html', {'form': form, 'action': 'Edit', 'member': member})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk, user=request.user)
    if request.method == 'POST':
        name = member.name
        member.delete()
        messages.success(request, f'{name} removed from your family.')
        return redirect('member_list')
    return render(request, 'members/confirm_delete.html', {'member': member})


# ─── HEALTH RECORD VIEWS ──────────────────────────────────────

@login_required
def record_add(request, member_pk):
    member = get_object_or_404(FamilyMember, pk=member_pk, user=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.family_member = member
            record.save()
            messages.success(request, 'Health record added!')
            return redirect('member_detail', pk=member_pk)
    else:
        form = HealthRecordForm()
    return render(request, 'records/form.html', {'form': form, 'member': member, 'action': 'Add'})


@login_required
def record_edit(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, family_member__user=request.user)
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated!')
            return redirect('member_detail', pk=record.family_member.pk)
    else:
        form = HealthRecordForm(instance=record)
    return render(request, 'records/form.html', {
        'form': form,
        'member': record.family_member,
        'action': 'Edit',
        'record': record
    })


@login_required
def record_delete(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, family_member__user=request.user)
    member_pk = record.family_member.pk
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted.')
        return redirect('member_detail', pk=member_pk)
    return render(request, 'records/confirm_delete.html', {'record': record})
