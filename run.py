import os
from app import create_app, db
from app.models import User, Department, Announcement

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.shell_context_processor
def make_shell_context():
    """Add database instance and models to shell context."""
    return {
        'db': db,
        'User': User,
        'Department': Department,
        'Announcement': Announcement
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
