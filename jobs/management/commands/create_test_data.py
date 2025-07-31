from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Profile, Job, Application

class Command(BaseCommand):
    help = 'Create test data for the job portal'

    def handle(self, *args, **options):
        # Create test employer
        employer_user = User.objects.create_user(
            username='testemployer',
            email='employer@test.com',
            password='testpass123',
            first_name='John',
            last_name='Employer'
        )
        Profile.objects.get_or_create(user=employer_user, defaults={'role': 'employer'})
        
        # Create test applicant
        applicant_user = User.objects.create_user(
            username='testapplicant',
            email='applicant@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Seeker'
        )
        Profile.objects.get_or_create(user=applicant_user, defaults={'role': 'applicant'})
        
        # Create test jobs
        job1 = Job.objects.create(
            title='Senior Python Developer',
            company_name='Tech Corp',
            location='New York, NY',
            description='We are looking for an experienced Python developer...',
            posted_by=employer_user
        )
        
        job2 = Job.objects.create(
            title='Frontend Developer',
            company_name='Web Solutions',
            location='San Francisco, CA',
            description='Join our team as a Frontend Developer using React...',
            posted_by=employer_user
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test data!\n'
                             'Employer: testemployer / testpass123\n'
                             'Applicant: testapplicant / testpass123')
        )
