from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            # Redirect based on user role
            if next_page:
                return redirect(next_page)
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'parent':
                return redirect(url_for('parent.dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role=form.role.data,
            student_id=form.student_id.data if form.role.data == 'student' else None,
            parent_student_id=form.parent_student_id.data if form.role.data == 'parent' else None
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
