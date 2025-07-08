#!/bin/bash

# GlobalMind FL - Development Setup Script
echo "🚀 Setting up GlobalMind FL Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ -z "$python_version" ]]; then
    print_error "Python 3.8+ is required but not found. Please install Python 3.8 or higher."
    exit 1
else
    print_status "Found Python $python_version"
fi

# Check if Node.js is installed
node_version=$(node --version 2>&1)
if [[ -z "$node_version" ]]; then
    print_error "Node.js is required but not found. Please install Node.js 16 or higher."
    exit 1
else
    print_status "Found Node.js $node_version"
fi

# Create virtual environment for backend
print_status "Creating Python virtual environment..."
cd backend
python3 -m venv globalmind_env
source globalmind_env/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p logs
mkdir -p models_cache
mkdir -p data/cultural_context

print_status "Backend setup completed!"

# Setup frontend
cd ../frontend
print_status "Installing Node.js dependencies..."
npm install

print_status "Frontend setup completed!"

# Return to root directory
cd ..

print_status "✅ GlobalMind FL setup completed successfully!"
echo ""
echo "🔧 To start the development environment:"
echo "1. Backend API Gateway:"
echo "   cd backend && source globalmind_env/bin/activate && python api/main.py"
echo ""
echo "2. Frontend (in a new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo ""
echo "📚 Check README.md for detailed instructions."
echo "🎯 Happy coding with GlobalMind FL!"
