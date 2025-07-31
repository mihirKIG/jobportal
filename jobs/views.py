from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Job, Application, Profile
from .forms import UserRegistrationForm, LoginForm, JobForm, ApplicationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.username}")
            print(f"Profile exists: {hasattr(user, 'profile')}")
            if hasattr(user, 'profile'):
                print(f"Profile role: {user.profile.role}")
            
            messages.success(request, f'Account created successfully for {user.username}! You can now log in.')
            return redirect('login')
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'jobs/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Ensure profile exists
                profile, created = Profile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'applicant'}
                )
                
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect based on role
                if profile.role == 'employer':
                    return redirect('employer_dashboard')
                else:
                    return redirect('applicant_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'jobs/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def employer_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'employer'}
    )
    
    if profile.role != 'employer':
        messages.error(request, 'Access denied. You are not an employer.')
        return redirect('job_list')
        
    jobs = Job.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

@login_required
def applicant_dashboard(request):
    """Enhanced applicant dashboard with status filtering"""
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'applicant'}
    )
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Get applications based on filter
    applications = Application.objects.filter(applicant=request.user)
    
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    applications = applications.order_by('-applied_at')
    
    # Calculate statistics
    all_applications = Application.objects.filter(applicant=request.user)
    stats = {
        'all': all_applications.count(),
        'pending': all_applications.filter(status='pending').count(),
        'approved': all_applications.filter(status='approved').count(),
        'rejected': all_applications.filter(status='rejected').count()
    }
    
    return render(request, 'jobs/applicant_dashboard.html', {
        'applications': applications,
        'stats': stats,
        'current_filter': status_filter
    })

@login_required
def post_job(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'employer'}
    )
    
    if profile.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')
        
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

def job_list(request):
    query = request.GET.get('q', '')
    jobs = Job.objects.all().order_by('-created_at')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        )
    
    # Calculate statistics
    job_stats = {
        'companies': jobs.values('company_name').distinct().count(),
        'locations': jobs.values('location').distinct().count(),
        'recent': jobs.filter(created_at__gte=datetime.now() - timedelta(days=7)).count(),
    }
    
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs, 
        'query': query,
        'job_stats': job_stats
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'applicant'}
    )
    
    if profile.role != 'applicant':
        messages.error(request, 'Only applicants can apply for jobs.')
        return redirect('job_detail', pk=pk)
    
    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
        
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def job_applications(request, pk):
    """View for employers to see all applications for a specific job they posted"""
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    
    # Ensure user is an employer
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'employer'}
    )
    
    if profile.role != 'employer':
        messages.error(request, 'Access denied. You are not an employer.')
        return redirect('job_list')
    
    # Get all applications for this job
    applications = Application.objects.filter(job=job).order_by('-applied_at')
    
    # Calculate statistics
    total_applications = applications.count()
    pending_count = applications.filter(status='pending').count()
    approved_count = applications.filter(status='approved').count()
    rejected_count = applications.filter(status='rejected').count()
    
    stats = {
        'total': total_applications,
        'pending': pending_count,
        'approved': approved_count,
        'rejected': rejected_count
    }
    
    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applications': applications,
        'stats': stats
    })

@login_required
def update_application_status(request, pk, status):
    """Update application status (approve/reject)"""
    application = get_object_or_404(Application, pk=pk)
    
    # Ensure the user is the employer who posted the job
    if application.job.posted_by != request.user:
        messages.error(request, 'You can only update applications for your own job postings.')
        return redirect('employer_dashboard')
    
    # Ensure status is valid
    if status not in ['approved', 'rejected', 'pending']:
        messages.error(request, 'Invalid status.')
        return redirect('job_applications', pk=application.job.pk)
    
    # Update the status
    old_status = application.status
    application.status = status
    application.save()
    
    # Success message
    applicant_name = f"{application.applicant.first_name} {application.applicant.last_name}".strip()
    if not applicant_name:
        applicant_name = application.applicant.username
    
    messages.success(request, f'Application from {applicant_name} has been {status}.')
    
    return redirect('job_applications', pk=application.job.pk)