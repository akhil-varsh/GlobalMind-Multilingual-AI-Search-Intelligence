@echo off
REM GlobalMind FL - Development Setup Script for Windows

echo 🚀 Setting up GlobalMind FL Development Environment...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3.8+ is required but not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is required but not found. Please install Node.js 16 or higher.
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
)

REM Setup backend
echo 📦 Setting up backend...
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv globalmind_env
call globalmind_env\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary directories
echo Creating directory structure...
if not exist "logs" mkdir logs
if not exist "models_cache" mkdir models_cache
if not exist "data\cultural_context" mkdir data\cultural_context

echo ✅ Backend setup completed!

REM Setup frontend
cd ..\frontend
echo 📦 Setting up frontend...
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup completed!

REM Return to root directory
cd ..

echo.
echo ✅ GlobalMind FL setup completed successfully!
echo.
echo 🔧 To start the development environment:
echo 1. Backend API Gateway (in Command Prompt):
echo    cd backend && globalmind_env\Scripts\activate && python api\main.py
echo.
echo 2. Frontend (in a new Command Prompt):
echo    cd frontend && npm start
echo.
echo 3. Access the application:
echo    Frontend: http://localhost:3000
echo    API: http://localhost:8000
echo.
echo 📚 Check README.md for detailed instructions.
echo 🎯 Happy coding with GlobalMind FL!
echo.
pause
