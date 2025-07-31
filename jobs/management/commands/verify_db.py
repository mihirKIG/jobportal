from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Profile, Job, Application
import logging

logger = logging.getLogger('jobs')

class Command(BaseCommand):
    help = 'Verify database state and user profiles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-missing-profiles',
            action='store_true',
            help='Create missing profiles for users without them',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Database State Verification'))
        self.stdout.write('=' * 50)
        
        # Check users and profiles
        total_users = User.objects.count()
        total_profiles = Profile.objects.count()
        
        self.stdout.write(f"📊 Total Users: {total_users}")
        self.stdout.write(f"📊 Total Profiles: {total_profiles}")
        
        # Find users without profiles
        users_without_profiles = []
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                users_without_profiles.append(user)
        
        if users_without_profiles:
            self.stdout.write(self.style.WARNING(f"⚠️  Users without profiles: {len(users_without_profiles)}"))
            for user in users_without_profiles:
                self.stdout.write(f"   - {user.username} (ID: {user.id})")
                
            if options['fix_missing_profiles']:
                self.stdout.write(self.style.WARNING("🔧 Creating missing profiles..."))
                for user in users_without_profiles:
                    Profile.objects.create(user=user, role='applicant')
                    self.stdout.write(f"   ✅ Created profile for {user.username}")
        else:
            self.stdout.write(self.style.SUCCESS("✅ All users have profiles"))
        
        # Show user details
        self.stdout.write("\n📋 User Details:")
        for user in User.objects.all():
            profile_info = "No Profile"
            if hasattr(user, 'profile'):
                profile_info = f"Role: {user.profile.role}"
            
            self.stdout.write(f"   👤 {user.username} | {user.email} | {profile_info}")
        
        # Show job statistics
        total_jobs = Job.objects.count()
        total_applications = Application.objects.count()
        
        self.stdout.write(f"\n💼 Total Jobs: {total_jobs}")
        self.stdout.write(f"📝 Total Applications: {total_applications}")
        
        # Show recent activity
        recent_users = User.objects.order_by('-date_joined')[:5]
        self.stdout.write("\n🆕 Recent Users:")
        for user in recent_users:
            self.stdout.write(f"   - {user.username} joined on {user.date_joined}")
        
        self.stdout.write(self.style.SUCCESS('\n✅ Verification Complete!'))
