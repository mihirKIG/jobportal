from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
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
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'applicant'}
    )
    
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'jobs/applicant_dashboard.html', {'applications': applications})

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