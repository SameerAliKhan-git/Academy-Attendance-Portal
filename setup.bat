@echo off
REM Setup script for Academy Attendance Portal on Windows

echo ========================================
echo Academy Attendance Portal - Setup
echo Team B - Web Dashboard Development
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [3/6] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Setting up environment variables...
if exist .env (
    echo .env file already exists, skipping...
) else (
    copy .env.example .env
    echo .env file created! Please edit it with your configuration.
)
echo.

echo [5/6] Creating upload directory...
if not exist "app\static\uploads" mkdir "app\static\uploads"
echo Upload directory ready!
echo.

echo [6/6] Initializing database...
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized successfully!')"
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Run the application with: python run.py
echo 3. Access at: http://localhost:5000
echo.
echo For more information, see README.md
echo ========================================
pause
