from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """User model for authentication and role management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, parent, teacher, admin
    student_id = db.Column(db.String(20), unique=True, nullable=True)  # For students
    parent_student_id = db.Column(db.String(20), nullable=True)  # For parents (linked student ID)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    department = db.relationship('Department', backref='users', lazy=True)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class Department(db.Model):
    """Department model for organizing users and announcements."""
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    announcements = db.relationship('Announcement', backref='department', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Announcement(db.Model):
    """Announcement model for departments to post updates."""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    announcement_type = db.Column(db.String(20), nullable=False)  # assignment, announcement, notice
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(256), nullable=True)  # Path to uploaded file
    file_name = db.Column(db.String(128), nullable=True)  # Original filename
    due_date = db.Column(db.DateTime, nullable=True)  # For assignments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    author = db.relationship('User', backref='announcements', lazy=True)
    
    def __repr__(self):
        return f'<Announcement {self.title} ({self.announcement_type})>'
