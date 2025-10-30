# Quick Start Guide - Academy Attendance Portal

## ⚡ Get Started in 5 Minutes

### For Windows Users

1. **Double-click `setup.bat`** to run the automated setup
   - Or open PowerShell and run: `.\setup.bat`

2. **Edit the `.env` file** (optional for development)
   - Default settings work for local testing

3. **Start the server**:
   ```powershell
   python run.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

5. **Create your first account**:
   - Click "Register"
   - Choose your role (Student, Parent, or Teacher)
   - Fill in the details and submit

That's it! 🎉

---

### For Linux/Mac Users

1. **Make setup script executable and run it**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Edit the `.env` file** (optional for development):
   ```bash
   nano .env
   ```

3. **Start the server**:
   ```bash
   python3 run.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

5. **Create your first account** via the registration page

---

## 🎯 Default Test Accounts

After running the setup, you can create these test accounts:

### Admin Account
```
Username: admin
Password: admin123
Role: Administrator
```

### Teacher Account
```
Username: teacher1
Password: teacher123
Role: Teacher
Department: Computer Science
```

### Student Account
```
Username: student1
Password: student123
Role: Student
Student ID: CS001
```

### Parent Account
```
Username: parent1
Password: parent123
Role: Parent
Linked Student ID: CS001
```

**⚠️ Important**: Change all default passwords in production!

---

## 📱 What Each Role Can Do

### Students
- ✅ View attendance percentage and history
- ✅ Access announcements and assignments
- ✅ Download shared files
- ✅ View department updates

### Parents
- ✅ Monitor child's attendance
- ✅ View all school communications
- ✅ Access assignments and due dates
- ✅ Download shared materials

### Teachers
- ✅ View department students
- ✅ Create announcements and assignments
- ✅ Upload files for students
- ✅ Manage attendance (when backend is connected)

### Admins
- ✅ Full system access
- ✅ User management
- ✅ Department administration
- ✅ System reports

---

## 🔧 Common First-Time Issues

### Issue: "Python not found"
**Solution**: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)

### Issue: "Module not found" errors
**Solution**: Make sure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Issue: "Port 5000 already in use"
**Solution**: Change the port in `run.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Issue: Can't create admin account
**Solution**: Use Python console:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@example.com',
        full_name='Administrator',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")
```

---

## 🎨 Customization Quick Tips

### Change the Site Name
Edit `app/templates/base.html`, line 15:
```html
<a class="navbar-brand" href="{{ url_for('main.index') }}">
    <i class="bi bi-calendar-check"></i> Your School Name
</a>
```

### Change Primary Color
Edit `app/static/css/style.css`, add at the top:
```css
:root {
    --bs-primary: #your-color-hex;
}
```

### Add Your Logo
1. Save logo as `app/static/images/logo.png`
2. Edit `base.html` navbar-brand:
```html
<a class="navbar-brand" href="{{ url_for('main.index') }}">
    <img src="{{ url_for('static', filename='images/logo.png') }}" 
         alt="Logo" height="30">
    Academy Attendance
</a>
```

---

## 📊 Sample Data Setup

To test with sample data, run:

```python
python3
>>> from app import create_app, db
>>> from app.models import User, Department, Announcement
>>> app = create_app()
>>> with app.app_context():
...     # Create department
...     dept = Department(name='Computer Science', code='CS', 
...                      description='CS Department')
...     db.session.add(dept)
...     db.session.flush()
...     
...     # Create teacher
...     teacher = User(username='teacher1', email='teacher@test.com',
...                   full_name='Jane Teacher', role='teacher',
...                   department_id=dept.id)
...     teacher.set_password('teacher123')
...     db.session.add(teacher)
...     db.session.flush()
...     
...     # Create announcement
...     announcement = Announcement(
...         title='Welcome to the System',
...         content='This is a test announcement for all students.',
...         announcement_type='announcement',
...         department_id=dept.id,
...         author_id=teacher.id
...     )
...     db.session.add(announcement)
...     db.session.commit()
...     print("Sample data created!")
```

---

## 🚀 Next Steps

1. **Explore the Dashboards**: Log in with different roles to see what each can do
2. **Read the Full README**: Check `README.md` for complete documentation
3. **Check API Docs**: See `API_DOCUMENTATION.md` for backend integration
4. **Deployment Guide**: See `DEPLOYMENT.md` for production setup

---

## 💡 Tips for Development

### Enable Debug Mode
Already enabled by default in `run.py`. You'll see:
- Detailed error pages
- Auto-reload on code changes
- Debug toolbar (if installed)

### View Database Content
```python
# Open Python console
python3

# View all users
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"{user.username} - {user.role}")
```

### Reset Database
```bash
# Delete database file
rm attendance.db  # Linux/Mac
del attendance.db  # Windows

# Recreate
python3
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

---

## 📞 Need Help?

- **Documentation**: Check README.md, API_DOCUMENTATION.md, DEPLOYMENT.md
- **Issues**: Review the troubleshooting section above
- **Contact**: Reach out to Team B development team

---

**Enjoy using Academy Attendance Portal! 🎓**

*Last Updated: October 30, 2025*
