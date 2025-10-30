from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from functools import wraps
import requests
from app.models import Announcement
from flask import current_app

student_bp = Blueprint('student', __name__)

def student_required(f):
    """Decorator to ensure user is a student."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'student':
            flash('Access denied. Students only.', 'danger')
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard showing attendance and announcements."""
    # Fetch attendance data from backend API
    attendance_data = fetch_attendance_data(current_user.student_id)
    
    # Get recent announcements
    announcements = Announcement.query.filter_by(is_active=True).order_by(
        Announcement.created_at.desc()
    ).limit(10).all()
    
    return render_template('student/dashboard.html', 
                         title='Student Dashboard',
                         attendance=attendance_data,
                         announcements=announcements)

@student_bp.route('/attendance')
@login_required
@student_required
def attendance():
    """Detailed attendance view."""
    attendance_data = fetch_attendance_data(current_user.student_id)
    attendance_logs = fetch_attendance_logs(current_user.student_id)
    
    return render_template('student/attendance.html',
                         title='My Attendance',
                         attendance=attendance_data,
                         logs=attendance_logs)

@student_bp.route('/announcements')
@login_required
@student_required
def announcements():
    """View all announcements."""
    all_announcements = Announcement.query.filter_by(is_active=True).order_by(
        Announcement.created_at.desc()
    ).all()
    
    return render_template('student/announcements.html',
                         title='Announcements',
                         announcements=all_announcements)

def fetch_attendance_data(student_id):
    """Fetch attendance percentage from backend API."""
    try:
        api_url = current_app.config['BACKEND_API_URL']
        response = requests.get(f'{api_url}/attendance/{student_id}', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {'percentage': 0, 'total_days': 0, 'present_days': 0, 'absent_days': 0}
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return {'percentage': 0, 'total_days': 0, 'present_days': 0, 'absent_days': 0}

def fetch_attendance_logs(student_id):
    """Fetch detailed attendance logs from backend API."""
    try:
        api_url = current_app.config['BACKEND_API_URL']
        response = requests.get(f'{api_url}/attendance/{student_id}/logs', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error fetching attendance logs: {e}")
        return []
