from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='Home')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Generic dashboard - redirects to role-specific dashboard."""
    if current_user.role == 'student':
        return redirect(url_for('student.dashboard'))
    elif current_user.role == 'parent':
        return redirect(url_for('parent.dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('teacher.dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('main.index'))

@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html', title='About')
