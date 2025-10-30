# Academy Attendance Portal - Team B Web Dashboard

A comprehensive Flask-based web dashboard for the Academy Attendance System, providing role-based interfaces for students, parents, teachers, and administrators.

## 🎯 Features

### Multi-Role Dashboard System
- **Student Dashboard**: View attendance percentage, detailed logs, and announcements
- **Parent Dashboard**: Monitor child's attendance and stay updated with school communications
- **Teacher Dashboard**: Manage students, mark attendance, and create announcements
- **Admin Dashboard**: System-wide management, user administration, and reporting

### Core Functionality
- ✅ Real-time attendance tracking and display
- 📢 Department announcements and updates system
- 📝 Assignment posting with due dates
- 🔔 Notice board for urgent communications
- 📎 File attachments for assignments and notices
- 🔐 Secure authentication with Flask-Login
- 📱 Fully responsive design (Bootstrap 5)
- 🎨 Modern UI with Bootstrap Icons

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy with SQLite (development)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF + WTForms
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Icons**: Bootstrap Icons
- **Templates**: Jinja2

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Academy Attendance Portal"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file with your settings
# Update SECRET_KEY, DATABASE_URI, and BACKEND_API_URL
```

### 5. Initialize Database
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
Academy Attendance Portal/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── forms.py                 # WTForms definitions
│   ├── routes/                  # Blueprint routes
│   │   ├── auth.py              # Authentication routes
│   │   ├── main.py              # Main routes
│   │   ├── student.py           # Student dashboard
│   │   ├── parent.py            # Parent dashboard
│   │   ├── teacher.py           # Teacher dashboard
│   │   ├── admin.py             # Admin dashboard
│   │   └── announcements.py     # Announcements module
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css        # Custom styles
│   │   ├── js/
│   │   │   └── main.js          # JavaScript functions
│   │   └── uploads/             # File uploads
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── index.html           # Home page
│       ├── auth/                # Authentication pages
│       ├── student/             # Student views
│       ├── parent/              # Parent views
│       ├── teacher/             # Teacher views
│       ├── admin/               # Admin views
│       └── announcements/       # Announcement views
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template
```

## 👥 User Roles & Access

### Student
- View personal attendance percentage and detailed logs
- Access all announcements, assignments, and notices
- Download attached files
- View department-specific updates

### Parent
- Monitor child's attendance (linked by student ID)
- View all school communications
- Access assignments and notices
- Download shared files

### Teacher
- View department students
- Mark and manage attendance
- Create announcements, assignments, and notices
- Upload files for students
- Manage own posts

### Admin
- Full system access
- User management (CRUD operations)
- Department management
- System reports and analytics
- Override permissions

## 🔧 Configuration

### Environment Variables (.env)
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URI=sqlite:///attendance.db
BACKEND_API_URL=http://localhost:5001/api
```

### Database Models
- **User**: Authentication and profile data
- **Department**: Organizational units
- **Announcement**: Posts, assignments, and notices

## 🌐 API Integration

The dashboard integrates with Team A's backend API for attendance data:

### Endpoints Used
- `GET /api/attendance/{student_id}` - Get attendance summary
- `GET /api/attendance/{student_id}/logs` - Get detailed logs

Update `BACKEND_API_URL` in `.env` to point to your backend API.

## 📱 Responsive Design

The dashboard is fully responsive and tested on:
- Desktop (1920x1080, 1366x768)
- Tablet (768x1024, iPad)
- Mobile (375x667, iPhone SE to iPhone 14 Pro Max)

## 🎨 UI/UX Features

- **Bootstrap 5**: Modern, responsive design
- **Bootstrap Icons**: 1500+ icons for clarity
- **Custom CSS**: Enhanced styling and animations
- **Dark Mode Ready**: Color scheme supports dark mode
- **Print Friendly**: Optimized print layouts for reports
- **Accessibility**: WCAG 2.1 compliant

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- File upload validation
- Role-based access control
- SQL injection prevention (SQLAlchemy ORM)

## 📊 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Role-based dashboard access
- [ ] Attendance data display
- [ ] Announcement creation and viewing
- [ ] File upload and download
- [ ] Responsive design on multiple devices
- [ ] Cross-browser compatibility

### Browser Compatibility
- ✅ Google Chrome (latest)
- ✅ Mozilla Firefox (latest)
- ✅ Microsoft Edge (latest)
- ✅ Safari (latest)

## 🚀 Deployment

### Production Considerations
1. Change `FLASK_ENV` to `production`
2. Use strong `SECRET_KEY`
3. Use PostgreSQL or MySQL instead of SQLite
4. Enable HTTPS
5. Configure proper WSGI server (Gunicorn, uWSGI)
6. Set up reverse proxy (Nginx, Apache)
7. Configure file upload limits
8. Enable logging and monitoring

### Example Deployment (Ubuntu + Nginx + Gunicorn)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Configure Nginx reverse proxy
# See deployment documentation for full setup
```

## 📝 Sample Data

### Creating Test Users
```python
from app import create_app, db
from app.models import User, Department

app = create_app()
with app.app_context():
    # Create department
    dept = Department(name='Computer Science', code='CS', description='CS Department')
    db.session.add(dept)
    
    # Create admin user
    admin = User(username='admin', email='admin@academy.edu', 
                 full_name='Admin User', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create student user
    student = User(username='student1', email='student1@academy.edu',
                   full_name='John Doe', role='student', student_id='CS001',
                   department_id=1)
    student.set_password('student123')
    db.session.add(student)
    
    db.session.commit()
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Database not found
```bash
# Solution: Initialize database
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

**Issue**: Module not found errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: Port already in use
```bash
# Solution: Change port in run.py or kill process
# Windows: netstat -ano | findstr :5000
# Linux: lsof -ti:5000 | xargs kill -9
```

## 📚 Additional Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Flask-Login Docs](https://flask-login.readthedocs.io/)

## 👨‍💻 Development Team

**Team B - Web & Dashboard Development**
- UI/UX Design & Implementation
- Flask Backend Development
- Database Design
- API Integration
- Testing & Documentation

## 📄 License

This project is part of the Academy Attendance System. All rights reserved.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/YourFeature`
2. Commit changes: `git commit -m 'Add YourFeature'`
3. Push to branch: `git push origin feature/YourFeature`
4. Submit pull request

## 📞 Support

For issues or questions, please contact the development team or create an issue in the repository.

---

**Last Updated**: October 30, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
>>>>>>> 4d3f718 (Initial commit: Academy Attendance Portal - Web Dashboard)
