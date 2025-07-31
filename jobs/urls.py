from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('applicant-dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('apply/<int:pk>/', views.apply_job, name='apply_job'),
]