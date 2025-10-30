# Deployment Guide - Academy Attendance Portal

## 🚀 Deployment Options

### Option 1: Local Development Server (Quick Start)

This is the simplest way to run the application for development and testing.

```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Run the Flask development server
python run.py
```

Access at: `http://localhost:5000`

**Note**: Do NOT use this for production!

---

### Option 2: Production Deployment (Recommended)

## Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+
- Nginx
- PostgreSQL (recommended) or MySQL
- Domain name (optional)

## Step-by-Step Production Deployment

### 1. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Install additional system dependencies
sudo apt install build-essential libpq-dev -y
```

### 2. Create Application User

```bash
# Create dedicated user for the app
sudo useradd -m -s /bin/bash academy
sudo passwd academy

# Switch to app user
sudo su - academy
```

### 3. Clone and Setup Application

```bash
# Clone repository
git clone <your-repo-url> academy-attendance
cd academy-attendance

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # For production
```

### 4. Configure PostgreSQL Database

```bash
# Switch to postgres user
sudo su - postgres

# Create database and user
psql
CREATE DATABASE academy_attendance;
CREATE USER academy_user WITH PASSWORD 'your_strong_password';
ALTER ROLE academy_user SET client_encoding TO 'utf8';
ALTER ROLE academy_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE academy_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE academy_attendance TO academy_user;
\q
exit
```

### 5. Configure Environment Variables

```bash
# Create production .env file
cat > .env << EOF
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URI=postgresql://academy_user:your_strong_password@localhost/academy_attendance
BACKEND_API_URL=https://api.yourdomain.com/api
EOF

# Secure the .env file
chmod 600 .env
```

### 6. Initialize Database

```bash
# Activate virtual environment
source venv/bin/activate

# Initialize database
python3 << EOF
from app import create_app, db
from app.models import User, Department

app = create_app('production')
with app.app_context():
    db.create_all()
    
    # Create default admin
    admin = User(
        username='admin',
        email='admin@yourdomain.com',
        full_name='System Administrator',
        role='admin'
    )
    admin.set_password('ChangeThisPassword123!')
    db.session.add(admin)
    db.session.commit()
    print("Database initialized successfully!")
EOF
```

### 7. Configure Gunicorn

```bash
# Create Gunicorn config file
cat > gunicorn_config.py << EOF
import multiprocessing

# Server socket
bind = "127.0.0.1:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/academy/academy-attendance/logs/access.log"
errorlog = "/home/academy/academy-attendance/logs/error.log"
loglevel = "info"

# Process naming
proc_name = "academy-attendance"

# Server mechanics
daemon = False
pidfile = "/home/academy/academy-attendance/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None
EOF

# Create logs directory
mkdir -p logs
```

### 8. Create Systemd Service

```bash
# Exit to root/sudo user
exit

# Create systemd service file
sudo nano /etc/systemd/system/academy-attendance.service
```

Add the following content:

```ini
[Unit]
Description=Academy Attendance Portal
After=network.target

[Service]
Type=notify
User=academy
Group=academy
WorkingDirectory=/home/academy/academy-attendance
Environment="PATH=/home/academy/academy-attendance/venv/bin"
ExecStart=/home/academy/academy-attendance/venv/bin/gunicorn --config gunicorn_config.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

```bash
# Reload systemd, enable and start service
sudo systemctl daemon-reload
sudo systemctl enable academy-attendance
sudo systemctl start academy-attendance
sudo systemctl status academy-attendance
```

### 9. Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/academy-attendance
```

Add the following:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static {
        alias /home/academy/academy-attendance/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Upload files
    location /uploads {
        alias /home/academy/academy-attendance/app/static/uploads;
        expires 7d;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Max upload size
    client_max_body_size 16M;
}
```

```bash
# Enable site and restart Nginx
sudo ln -s /etc/nginx/sites-available/academy-attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### 11. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## 📱 Alternative Deployment Options

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create academy-attendance

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Create Procfile
echo "web: gunicorn run:app" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Initialize database
heroku run python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

### Deploy to AWS EC2

Similar to production deployment above, but:
1. Launch EC2 instance (Ubuntu 20.04 LTS)
2. Configure security groups (ports 80, 443, 22)
3. Assign Elastic IP
4. Follow production deployment steps
5. Use RDS for PostgreSQL database

### Deploy to Google Cloud Platform

```bash
# Use Google Cloud Run
gcloud run deploy academy-attendance \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

---

## 🔧 Post-Deployment Tasks

### 1. Create Admin Account
```bash
python3 << EOF
from app import create_app, db
from app.models import User

app = create_app('production')
with app.app_context():
    admin = User(
        username='admin',
        email='admin@yourdomain.com',
        full_name='Administrator',
        role='admin'
    )
    admin.set_password('SecurePassword123!')
    db.session.add(admin)
    db.session.commit()
EOF
```

### 2. Setup Backup System
```bash
# Create backup script
cat > /home/academy/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/academy/backups"
mkdir -p $BACKUP_DIR

# Backup database
pg_dump academy_attendance > "$BACKUP_DIR/db_$DATE.sql"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /home/academy/academy-attendance/app/static/uploads/

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /home/academy/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/academy/backup.sh") | crontab -
```

### 3. Monitoring

```bash
# Install monitoring tools
sudo apt install htop nethogs -y

# Check application logs
sudo journalctl -u academy-attendance -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check Gunicorn logs
tail -f /home/academy/academy-attendance/logs/error.log
```

---

## 🔄 Updates and Maintenance

### Update Application

```bash
# Stop service
sudo systemctl stop academy-attendance

# Pull latest code
cd /home/academy/academy-attendance
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations if needed
flask db upgrade

# Restart service
sudo systemctl start academy-attendance
```

### Database Migrations (Flask-Migrate)

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 📊 Performance Optimization

1. **Use CDN** for static assets
2. **Enable caching** with Redis/Memcached
3. **Optimize images** before upload
4. **Use connection pooling** for database
5. **Enable Gzip compression** in Nginx
6. **Implement rate limiting**

---

## 🛡️ Security Checklist

- [ ] Strong SECRET_KEY set
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Firewall configured (UFW/iptables)
- [ ] Database password is strong and unique
- [ ] File upload validation enabled
- [ ] CSRF protection active
- [ ] SQL injection prevention (using ORM)
- [ ] XSS protection headers set
- [ ] Regular security updates
- [ ] Backup system configured
- [ ] Monitoring and logging enabled

---

## 📞 Support

For deployment issues, contact the development team or refer to:
- Flask Deployment: https://flask.palletsprojects.com/en/3.0.x/deploying/
- Gunicorn Docs: https://docs.gunicorn.org/
- Nginx Docs: https://nginx.org/en/docs/

**Last Updated**: October 30, 2025
