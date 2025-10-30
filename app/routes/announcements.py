from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Announcement
from app.forms import AnnouncementForm
import os

announcements_bp = Blueprint('announcements', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@announcements_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new announcement, assignment, or notice."""
    if current_user.role not in ['teacher', 'admin']:
        flash('Only teachers and admins can create announcements.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if not current_user.department:
        flash('You must be assigned to a department to create announcements.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        # Handle file upload
        file_path = None
        file_name = None
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename
                import uuid
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                file_name = filename
            else:
                flash('Invalid file type.', 'danger')
                return render_template('announcements/create.html', form=form)
        
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            announcement_type=form.announcement_type.data,
            department_id=current_user.department_id,
            author_id=current_user.id,
            file_path=file_path,
            file_name=file_name,
            due_date=form.due_date.data if form.announcement_type.data == 'assignment' else None
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash(f'{form.announcement_type.data.capitalize()} created successfully!', 'success')
        return redirect(url_for('announcements.view', announcement_id=announcement.id))
    
    return render_template('announcements/create.html',
                         title='Create Announcement',
                         form=form)

@announcements_bp.route('/view/<int:announcement_id>')
@login_required
def view(announcement_id):
    """View specific announcement."""
    announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('announcements/view.html',
                         title=announcement.title,
                         announcement=announcement)

@announcements_bp.route('/list')
@login_required
def list_all():
    """List all announcements."""
    announcement_type = request.args.get('type', 'all')
    
    query = Announcement.query.filter_by(is_active=True)
    
    if announcement_type != 'all':
        query = query.filter_by(announcement_type=announcement_type)
    
    all_announcements = query.order_by(Announcement.created_at.desc()).all()
    
    return render_template('announcements/list.html',
                         title='All Announcements',
                         announcements=all_announcements,
                         current_type=announcement_type)

@announcements_bp.route('/delete/<int:announcement_id>', methods=['POST'])
@login_required
def delete(announcement_id):
    """Delete announcement (soft delete)."""
    announcement = Announcement.query.get_or_404(announcement_id)
    
    # Check if user has permission to delete
    if current_user.id != announcement.author_id and current_user.role != 'admin':
        flash('You do not have permission to delete this announcement.', 'danger')
        return redirect(url_for('announcements.view', announcement_id=announcement_id))
    
    announcement.is_active = False
    db.session.commit()
    
    flash('Announcement deleted successfully.', 'success')
    return redirect(url_for('announcements.list_all'))
