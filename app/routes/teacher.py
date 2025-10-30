from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
import requests
from app.models import Announcement, User
from flask import current_app

teacher_bp = Blueprint('teacher', __name__)

def teacher_required(f):
    """Decorator to ensure user is a teacher."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['teacher', 'admin']:
            flash('Access denied. Teachers only.', 'danger')
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """Teacher dashboard showing department info and announcements."""
    # Get students count from department
    students_count = 0
    if current_user.department:
        students_count = User.query.filter_by(
            department_id=current_user.department_id,
            role='student',
            is_active=True
        ).count()
    
    # Get recent announcements from this teacher
    my_announcements = Announcement.query.filter_by(
        author_id=current_user.id,
        is_active=True
    ).order_by(Announcement.created_at.desc()).limit(5).all()
    
    return render_template('teacher/dashboard.html',
                         title='Teacher Dashboard',
                         students_count=students_count,
                         announcements=my_announcements)

@teacher_bp.route('/students')
@login_required
@teacher_required
def students():
    """View students in department."""
    if not current_user.department:
        flash('You are not assigned to any department.', 'warning')
        return redirect(url_for('teacher.dashboard'))
    
    department_students = User.query.filter_by(
        department_id=current_user.department_id,
        role='student',
        is_active=True
    ).all()
    
    return render_template('teacher/students.html',
                         title='Students',
                         students=department_students)

@teacher_bp.route('/attendance')
@login_required
@teacher_required
def attendance():
    """View and manage attendance."""
    # This would integrate with the backend API to mark attendance
    return render_template('teacher/attendance.html',
                         title='Manage Attendance')
