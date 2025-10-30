from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=128)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher')
    ], validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[Optional(), Length(max=20)])
    parent_student_id = StringField('Student ID (for Parent)', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class AnnouncementForm(FlaskForm):
    """Form for creating announcements, assignments, and notices."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    announcement_type = SelectField('Type', choices=[
        ('announcement', 'Announcement'),
        ('assignment', 'Assignment'),
        ('notice', 'Notice')
    ], validators=[DataRequired()])
    due_date = DateTimeField('Due Date (for Assignments)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    file = FileField('Attach File (Optional)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'], 'Invalid file type!')
    ])
    submit = SubmitField('Post')
