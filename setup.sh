#!/bin/bash
# Setup script for Academy Attendance Portal on Linux/Mac

echo "========================================"
echo "Academy Attendance Portal - Setup"
echo "Team B - Web Dashboard Development"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi
echo ""

echo "[2/6] Activating virtual environment..."
source venv/bin/activate
echo ""

echo "[3/6] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo ""

echo "[4/6] Setting up environment variables..."
if [ -f ".env" ]; then
    echo ".env file already exists, skipping..."
else
    cp .env.example .env
    echo ".env file created! Please edit it with your configuration."
fi
echo ""

echo "[5/6] Creating upload directory..."
mkdir -p app/static/uploads
echo "Upload directory ready!"
echo ""

echo "[6/6] Initializing database..."
python3 << EOF
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
EOF

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run the application with: python3 run.py"
echo "3. Access at: http://localhost:5000"
echo ""
echo "For more information, see README.md"
echo "========================================"
