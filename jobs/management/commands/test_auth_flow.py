from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from jobs.models import Profile
import json

class Command(BaseCommand):
    help = 'Test registration and login flow with detailed logging'

    def handle(self, *args, **options):
        client = Client()
        
        self.stdout.write(self.style.SUCCESS('🧪 Testing Registration Flow'))
        self.stdout.write('=' * 50)
        
        # Test data
        test_user_data = {
            'username': 'testuser2025',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser2025@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'role': 'employer',
            'terms_agreed': True
        }
        
        # Step 1: Test AJAX username availability
        self.stdout.write("🔍 Step 1: Testing username availability check...")
        response = client.post('/api/check-username/', 
                               json.dumps({'username': test_user_data['username']}),
                               content_type='application/json')
        self.stdout.write(f"   Username check response: {response.json()}")
        
        # Step 2: Test AJAX email availability
        self.stdout.write("🔍 Step 2: Testing email availability check...")
        response = client.post('/api/check-email/', 
                               json.dumps({'email': test_user_data['email']}),
                               content_type='application/json')
        self.stdout.write(f"   Email check response: {response.json()}")
        
        # Step 3: Test registration form submission
        self.stdout.write("🔍 Step 3: Testing registration form submission...")
        response = client.post('/register/', test_user_data)
        
        if response.status_code == 302:  # Redirect after successful registration
            self.stdout.write(self.style.SUCCESS("   ✅ Registration successful!"))
            self.stdout.write(f"   Redirect to: {response.url}")
            
            # Check if user was created
            try:
                user = User.objects.get(username=test_user_data['username'])
                self.stdout.write(f"   ✅ User created: {user.username} (ID: {user.id})")
                self.stdout.write(f"   Email: {user.email}")
                self.stdout.write(f"   Name: {user.first_name} {user.last_name}")
                
                # Check profile
                if hasattr(user, 'profile'):
                    self.stdout.write(f"   ✅ Profile created with role: {user.profile.role}")
                else:
                    self.stdout.write(self.style.ERROR("   ❌ Profile not created!"))
                    
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("   ❌ User not found in database!"))
        else:
            self.stdout.write(self.style.ERROR(f"   ❌ Registration failed with status: {response.status_code}"))
            self.stdout.write(f"   Response content: {response.content.decode()[:500]}...")
        
        # Step 4: Test login
        self.stdout.write("\n🔍 Step 4: Testing login...")
        login_data = {
            'username': test_user_data['username'],
            'password': test_user_data['password1'],
            'remember_me': True
        }
        
        response = client.post('/login/', login_data)
        if response.status_code == 302:
            self.stdout.write(self.style.SUCCESS("   ✅ Login successful!"))
            self.stdout.write(f"   Redirect to: {response.url}")
        else:
            self.stdout.write(self.style.ERROR(f"   ❌ Login failed with status: {response.status_code}"))
        
        # Step 5: Test dashboard access
        self.stdout.write("\n🔍 Step 5: Testing dashboard access...")
        if test_user_data['role'] == 'employer':
            response = client.get('/employer/dashboard/')
        else:
            response = client.get('/applicant/dashboard/')
            
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   ✅ Dashboard access successful!"))
        else:
            self.stdout.write(self.style.ERROR(f"   ❌ Dashboard access failed: {response.status_code}"))
        
        # Final verification
        self.stdout.write("\n📊 Final Database State:")
        total_users = User.objects.count()
        total_profiles = Profile.objects.count()
        self.stdout.write(f"   Total Users: {total_users}")
        self.stdout.write(f"   Total Profiles: {total_profiles}")
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test Complete!'))
