# 🏗️ Architecture Overview - Academy Attendance Portal

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                               │
├─────────────┬─────────────┬─────────────┬─────────────────────────┤
│   Student   │   Parent    │   Teacher   │        Admin            │
│  Dashboard  │  Dashboard  │  Dashboard  │       Dashboard         │
└──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────────────────┘
       │             │             │             │
       └─────────────┴─────────────┴─────────────┘
                     │
       ┌─────────────▼─────────────────────────────┐
       │        Flask Web Application              │
       │  (Team B - Web Dashboard Development)     │
       ├───────────────────────────────────────────┤
       │  ┌─────────────────────────────────────┐  │
       │  │         Flask Blueprints            │  │
       │  ├─────────────────────────────────────┤  │
       │  │  • auth.py    (Login/Register)     │  │
       │  │  • main.py    (Home/About)         │  │
       │  │  • student.py  (Student Views)     │  │
       │  │  • parent.py   (Parent Views)      │  │
       │  │  • teacher.py  (Teacher Views)     │  │
       │  │  • admin.py    (Admin Views)       │  │
       │  │  • announcements.py (Posts)        │  │
       │  └─────────────────────────────────────┘  │
       │                                            │
       │  ┌─────────────────────────────────────┐  │
       │  │      Business Logic Layer           │  │
       │  ├─────────────────────────────────────┤  │
       │  │  • Flask-Login (Authentication)    │  │
       │  │  • Flask-WTF  (Form Handling)      │  │
       │  │  • Werkzeug   (Security)           │  │
       │  └─────────────────────────────────────┘  │
       │                                            │
       │  ┌─────────────────────────────────────┐  │
       │  │       Data Access Layer             │  │
       │  ├─────────────────────────────────────┤  │
       │  │  • SQLAlchemy ORM                  │  │
       │  │  • Models: User, Department,       │  │
       │  │    Announcement                     │  │
       │  └─────────────────────────────────────┘  │
       └──────────────┬──────────────┬─────────────┘
                      │              │
        ┌─────────────▼──────┐   ┌───▼──────────────────┐
        │   Local Database   │   │   Backend API        │
        │   (SQLite/         │   │   (Team A)           │
        │    PostgreSQL)     │   │                      │
        │                    │   │  • Attendance Data   │
        │  • Users           │   │  • Student Records   │
        │  • Departments     │   │  • Logs              │
        │  • Announcements   │   │                      │
        └────────────────────┘   └──────────────────────┘
```

---

## Request Flow Diagram

### User Login Flow
```
User Browser
    │
    ├─→ GET /login
    │   └─→ Flask Route (auth.py)
    │       └─→ Render login.html
    │
    ├─→ POST /login (credentials)
    │   └─→ Flask Route (auth.py)
    │       └─→ Validate with User Model
    │           └─→ Flask-Login authenticate
    │               └─→ Redirect to dashboard
    │
    └─→ GET /student/dashboard (or /parent/, /teacher/, /admin/)
        └─→ Flask Route (role-specific blueprint)
            ├─→ Check authentication (@login_required)
            ├─→ Check role permissions (@student_required, etc.)
            ├─→ Fetch data from database
            ├─→ Call Backend API (if needed)
            └─→ Render dashboard template
```

### Announcement Creation Flow
```
Teacher Browser
    │
    ├─→ GET /announcements/create
    │   └─→ Flask Route (announcements.py)
    │       └─→ Check auth & permissions
    │           └─→ Render create form
    │
    └─→ POST /announcements/create (form data + file)
        └─→ Flask Route (announcements.py)
            ├─→ Validate form (Flask-WTF)
            ├─→ Validate file upload
            ├─→ Save file to uploads/
            ├─→ Create Announcement model
            ├─→ Save to database
            └─→ Redirect to view page
```

### Attendance Display Flow
```
Student Browser
    │
    └─→ GET /student/attendance
        └─→ Flask Route (student.py)
            ├─→ Check authentication
            ├─→ Check student role
            ├─→ Fetch student_id from session
            ├─→ Call Backend API
            │   └─→ GET /api/attendance/{student_id}
            │       └─→ Return JSON data
            ├─→ Parse API response
            ├─→ Fetch logs from API
            │   └─→ GET /api/attendance/{student_id}/logs
            │       └─→ Return JSON array
            └─→ Render attendance.html with data
```

---

## Database Schema

```
┌─────────────────────────────────────┐
│             users                   │
├─────────────────────────────────────┤
│ id (PK)                 INTEGER     │
│ username                VARCHAR(64) │
│ email                   VARCHAR(120)│
│ password_hash           VARCHAR(256)│
│ full_name               VARCHAR(128)│
│ role                    VARCHAR(20) │
│ student_id              VARCHAR(20) │
│ parent_student_id       VARCHAR(20) │
│ department_id (FK)      INTEGER     │
│ created_at              DATETIME    │
│ is_active               BOOLEAN     │
└──────────────┬──────────────────────┘
               │
               │ (Many-to-One)
               │
┌──────────────▼──────────────────────┐
│          departments                │
├─────────────────────────────────────┤
│ id (PK)                 INTEGER     │
│ name                    VARCHAR(100)│
│ code                    VARCHAR(10) │
│ description             TEXT        │
│ created_at              DATETIME    │
└──────────────┬──────────────────────┘
               │
               │ (One-to-Many)
               │
┌──────────────▼──────────────────────┐
│          announcements              │
├─────────────────────────────────────┤
│ id (PK)                 INTEGER     │
│ title                   VARCHAR(200)│
│ content                 TEXT        │
│ announcement_type       VARCHAR(20) │
│ department_id (FK)      INTEGER     │
│ author_id (FK)          INTEGER     │
│ file_path               VARCHAR(256)│
│ file_name               VARCHAR(128)│
│ due_date                DATETIME    │
│ created_at              DATETIME    │
│ updated_at              DATETIME    │
│ is_active               BOOLEAN     │
└─────────────────────────────────────┘
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Client)                      │
├─────────────────────────────────────────────────────────┤
│  • HTML (Jinja2 Templates)                              │
│  • CSS (Bootstrap 5 + Custom)                           │
│  • JavaScript (Vanilla JS + Bootstrap JS)               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Nginx (Reverse Proxy)                   │
│                   [Production Only]                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         Gunicorn (WSGI Server) [Production]             │
│            or Flask Dev Server [Development]             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Flask Application                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Routes     │  │    Forms     │  │   Models     │  │
│  │  (Blueprints)│◄─┤  (WTForms)   │  │ (SQLAlchemy) │  │
│  └──────────────┘  └──────────────┘  └──────┬───────┘  │
│         │                                     │          │
│         │          ┌──────────────┐          │          │
│         └─────────►│  Templates   │          │          │
│                    │   (Jinja2)   │          │          │
│                    └──────────────┘          │          │
│                                              │          │
└──────────────────────────────────────────────┼──────────┘
                                               │
                     ┌─────────────────────────┼──────────┐
                     │                         │          │
            ┌────────▼────────┐    ┌───────────▼────────┐ │
            │   Database      │    │   External API     │ │
            │   (SQLite/      │    │   (Backend Team A) │ │
            │   PostgreSQL)   │    │                    │ │
            └─────────────────┘    └────────────────────┘ │
                                                           │
                     ┌─────────────────────────────────────┘
                     │
            ┌────────▼────────┐
            │  File Storage   │
            │  (Uploads)      │
            └─────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: Network Security                              │
│  ┌────────────────────────────────────────────────┐    │
│  │ • HTTPS/SSL (Let's Encrypt)                    │    │
│  │ • Firewall (UFW)                               │    │
│  │ • Rate Limiting (Nginx)                        │    │
│  └────────────────────────────────────────────────┘    │
│                          ▼                              │
│  Layer 2: Application Security                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ • CSRF Protection (Flask-WTF)                  │    │
│  │ • XSS Headers                                  │    │
│  │ • Session Management (Flask-Login)             │    │
│  │ • Password Hashing (Werkzeug)                  │    │
│  └────────────────────────────────────────────────┘    │
│                          ▼                              │
│  Layer 3: Authorization                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │ • Role-Based Access Control                    │    │
│  │ • Route Decorators (@login_required)           │    │
│  │ • Permission Checks (role verification)        │    │
│  └────────────────────────────────────────────────┘    │
│                          ▼                              │
│  Layer 4: Data Security                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │ • SQL Injection Prevention (ORM)               │    │
│  │ • File Upload Validation                       │    │
│  │ • Input Sanitization                           │    │
│  │ • Environment Variables (.env)                 │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Development Environment
```
Developer Machine
    │
    └─→ Flask Development Server
        ├─→ SQLite Database
        ├─→ Local File Storage
        └─→ Mock API Responses
```

### Production Environment
```
                    Internet
                       │
                       ▼
              ┌────────────────┐
              │   CloudFlare   │ (CDN/DDoS Protection)
              │   or similar   │
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │  Load Balancer │ (Optional, for scaling)
              └────────┬───────┘
                       │
           ┌───────────┴───────────┐
           │                       │
    ┌──────▼──────┐         ┌─────▼───────┐
    │  Server 1   │         │  Server 2   │ (Optional)
    │   Ubuntu    │         │   Ubuntu    │
    ├─────────────┤         ├─────────────┤
    │   Nginx     │         │   Nginx     │
    │      ▼      │         │      ▼      │
    │  Gunicorn   │         │  Gunicorn   │
    │      ▼      │         │      ▼      │
    │   Flask     │         │   Flask     │
    └──────┬──────┘         └──────┬──────┘
           │                       │
           └───────────┬───────────┘
                       │
                ┌──────▼──────┐
                │ PostgreSQL  │ (Primary Database)
                │  Database   │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │   Backup    │ (Daily automated)
                │  Database   │
                └─────────────┘
                       
                ┌─────────────┐
                │     S3/     │ (File Storage, optional)
                │   Storage   │
                └─────────────┘
```

---

## File Structure Visualization

```
Academy Attendance Portal/
│
├── 📚 Documentation Files
│   ├── README.md                  (Main documentation)
│   ├── QUICKSTART.md              (Quick start guide)
│   ├── DEPLOYMENT.md              (Deployment guide)
│   ├── API_DOCUMENTATION.md       (API specs)
│   ├── PROJECT_SUMMARY.md         (Project overview)
│   ├── ARCHITECTURE.md            (This file)
│   └── INDEX.md                   (Documentation index)
│
├── ⚙️ Configuration Files
│   ├── config.py                  (App configuration)
│   ├── .env.example               (Environment template)
│   ├── requirements.txt           (Dependencies)
│   └── .gitignore                 (Git exclusions)
│
├── 🚀 Entry Points
│   ├── run.py                     (Application runner)
│   ├── setup.bat                  (Windows setup)
│   └── setup.sh                   (Linux/Mac setup)
│
└── 📦 Application Package (app/)
    │
    ├── __init__.py                (App factory)
    ├── models.py                  (Database models)
    ├── forms.py                   (Form definitions)
    │
    ├── 🛣️ routes/                 (URL handlers)
    │   ├── auth.py                (Authentication)
    │   ├── main.py                (General pages)
    │   ├── student.py             (Student features)
    │   ├── parent.py              (Parent features)
    │   ├── teacher.py             (Teacher features)
    │   ├── admin.py               (Admin features)
    │   └── announcements.py       (Announcements)
    │
    ├── 🎨 static/                 (Static assets)
    │   ├── css/
    │   │   └── style.css          (Custom styles)
    │   ├── js/
    │   │   └── main.js            (JavaScript)
    │   └── uploads/               (User files)
    │
    └── 🖼️ templates/              (HTML templates)
        ├── base.html              (Base layout)
        ├── index.html             (Home page)
        ├── auth/                  (Login/Register)
        ├── student/               (Student views)
        ├── parent/                (Parent views)
        ├── teacher/               (Teacher views)
        ├── admin/                 (Admin views)
        ├── announcements/         (Announcement views)
        ├── main/                  (General pages)
        └── errors/                (Error pages)
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
├─────────────────────────────────────────────────────────┤
│  HTML5 │ CSS3 │ Bootstrap 5 │ Bootstrap Icons │ JS     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Template Layer                        │
├─────────────────────────────────────────────────────────┤
│                    Jinja2 Templates                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Application Layer                      │
├─────────────────────────────────────────────────────────┤
│  Flask 3.0 │ Blueprints │ Flask-Login │ Flask-WTF      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Data Access Layer                       │
├─────────────────────────────────────────────────────────┤
│  SQLAlchemy ORM │ Models │ Queries │ Relationships     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Database Layer                         │
├─────────────────────────────────────────────────────────┤
│  SQLite (Dev) │ PostgreSQL (Prod) │ MySQL (Alt)        │
└─────────────────────────────────────────────────────────┘
```

---

## API Integration Points

```
Flask Dashboard (Team B)          Backend API (Team A)
        │                                 │
        │  GET /api/attendance/{id}       │
        ├────────────────────────────────►│
        │                                 │
        │  Response: Attendance Summary   │
        │◄────────────────────────────────┤
        │                                 │
        │  GET /api/attendance/{id}/logs  │
        ├────────────────────────────────►│
        │                                 │
        │  Response: Attendance Logs      │
        │◄────────────────────────────────┤
        │                                 │
        │  POST /api/attendance/mark      │
        ├────────────────────────────────►│
        │                                 │
        │  Response: Success/Failure      │
        │◄────────────────────────────────┤
        │                                 │
```

---

## Performance Optimization Strategy

```
┌─────────────────────────────────────────────────────────┐
│              Performance Optimization                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend:                                              │
│  • Minified CSS/JS                                      │
│  • CDN for Bootstrap & Icons                            │
│  • Image optimization                                    │
│  • Lazy loading                                          │
│  • Browser caching                                       │
│                                                          │
│  Backend:                                               │
│  • Database query optimization                           │
│  • Connection pooling                                    │
│  • Response caching                                      │
│  • Async operations                                      │
│  • Load balancing                                        │
│                                                          │
│  Infrastructure:                                        │
│  • Nginx caching                                         │
│  • Gzip compression                                      │
│  • Static file serving                                   │
│  • CDN integration                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

**This architecture supports:**
- ✅ Scalability (horizontal & vertical)
- ✅ Security (multiple layers)
- ✅ Maintainability (modular design)
- ✅ Performance (optimized at all layers)
- ✅ Extensibility (easy to add features)

---

*Last Updated: October 30, 2025*
*Team B - Web & Dashboard Development*
