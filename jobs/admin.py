from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Job, Application, Profile

# Profile Inline for User Admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('role', 'phone', 'address', 'created_at')
    readonly_fields = ('created_at',)

# Extended User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'date_joined', 'is_active')
    list_filter = ('is_active', 'is_staff', 'date_joined', 'profile__role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    def get_role(self, obj):
        try:
            return obj.profile.role.title()
        except Profile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'user_email', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'posted_by', 'created_at', 'get_applications_count')
    list_filter = ('created_at', 'location', 'company_name')
    search_fields = ('title', 'company_name', 'location', 'description', 'posted_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    get_applications_count.short_description = 'Applications'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applicant_email', 'applicant_phone', 'applied_at')
    list_filter = ('applied_at', 'job__company_name')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at',)
    
    def applicant_email(self, obj):
        return obj.applicant.email
    applicant_email.short_description = 'Applicant Email'
    
    def applicant_phone(self, obj):
        try:
            return obj.applicant.profile.phone
        except Profile.DoesNotExist:
            return 'N/A'
    applicant_phone.short_description = 'Phone'

# Customize Admin Site
admin.site.site_header = "Job Portal Administration"
admin.site.site_title = "Job Portal Admin"
admin.site.index_title = "Welcome to Job Portal Administration"