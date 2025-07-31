# Django Job Portal

A comprehensive job portal web application built with Django 5.1.3 featuring complete user authentication, role-based access control, and modern responsive design.

## Features

### 🔐 Authentication System
- **User Registration** with email verification
- **Secure Login/Logout** functionality
- **Role-based Access Control** (Employer/Applicant)
- **Profile Management** with customizable user profiles
- **Password Security** with strength validation

### 💼 For Employers
- **Post Job Listings** with detailed descriptions
- **Manage Posted Jobs** (view, edit, delete)
- **View Job Applications** from candidates
- **Employer Dashboard** with application analytics

### 👤 For Job Seekers
- **Browse Job Listings** with search and filter options
- **Apply for Jobs** with resume upload
- **Application Tracking** (view application status)
- **Applicant Dashboard** with applied jobs overview

### 🎨 Modern UI/UX
- **Bootstrap 5.3.2** responsive design
- **Font Awesome Icons** for better visual experience
- **Clean and Intuitive Interface**
- **Mobile-friendly** responsive layout

## Technology Stack

- **Backend**: Django 5.1.3
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3.2
- **Icons**: Font Awesome 6
- **Authentication**: Django's built-in auth system with custom extensions

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/MihirKantiRoy/jobportalrepo.git
   cd jobportalrepo
   ```

2. **Create virtual environment**
   ```bash
   python -m venv job
   ```

3. **Activate virtual environment**
   - Windows: `job\Scripts\activate`
   - macOS/Linux: `source job/bin/activate`

4. **Install dependencies**
   ```bash
   pip install django
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
jobportal/
├── jobportal/          # Django project settings
│   ├── settings.py     # Main settings
│   ├── urls.py         # URL routing
│   └── ...
├── jobs/               # Main application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   ├── urls.py         # App URL routing
│   ├── templates/      # HTML templates
│   └── ...
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Key Features Implemented

### Authentication & Security
- Custom user registration with profile creation
- Real-time form validation
- Secure password handling
- Session management
- CSRF protection

### Database Models
- **User**: Extended Django user model
- **Profile**: User profile with role-based access
- **Job**: Job listing model with employer relationship
- **Application**: Job application tracking

### Views & Templates
- **Class-based views** for better code organization
- **Template inheritance** for consistent design
- **Responsive templates** for all device types
- **Form handling** with proper error display

## Usage

### For Employers
1. Register as an "Employer"
2. Complete your profile
3. Post job listings
4. Review applications from job seekers

### For Job Seekers  
1. Register as an "Applicant"
2. Complete your profile
3. Browse and search job listings
4. Apply for jobs with resume upload

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Developer**: Mihir Kanti Roy
- **GitHub**: [@MihirKantiRoy](https://github.com/MihirKantiRoy)
- **Repository**: [jobportalrepo](https://github.com/MihirKantiRoy/jobportalrepo)

## Acknowledgments

- Django framework for robust web development
- Bootstrap for responsive UI components
- Font Awesome for beautiful icons
- Community contributors and testers
