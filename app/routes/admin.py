from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Department, Announcement
from app import db

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to ensure user is an admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. Admins only.', 'danger')
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with system overview."""
    # Get system statistics
    stats = {
        'total_users': User.query.count(),
        'students': User.query.filter_by(role='student', is_active=True).count(),
        'parents': User.query.filter_by(role='parent', is_active=True).count(),
        'teachers': User.query.filter_by(role='teacher', is_active=True).count(),
        'departments': Department.query.count(),
        'announcements': Announcement.query.filter_by(is_active=True).count()
    }
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         stats=stats,
                         recent_users=recent_users)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """View and manage all users."""
    all_users = User.query.all()
    return render_template('admin/users.html',
                         title='Manage Users',
                         users=all_users)

@admin_bp.route('/departments')
@login_required
@admin_required
def departments():
    """View and manage departments."""
    all_departments = Department.query.all()
    return render_template('admin/departments.html',
                         title='Manage Departments',
                         departments=all_departments)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """Generate system reports."""
    return render_template('admin/reports.html',
                         title='System Reports')
