#!/bin/bash
# Quick start script for SAM3 Web Application

set -e

echo "🚀 SAM3 Web Application - Quick Start"
echo "======================================"

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [ "$python_version" != "3.12" ]; then
    echo "⚠️  Warning: Python 3.12 is recommended, but found Python $python_version"
fi

# Check Node.js
echo ""
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ for frontend development."
    exit 1
fi
echo "✓ Node.js $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi
echo "✓ npm $(npm --version)"

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..
echo "✓ Backend dependencies installed"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..
echo "✓ Frontend dependencies installed"

# Build frontend
echo ""
echo "🔨 Building frontend..."
cd frontend
npm run build
cd ..
echo "✓ Frontend built successfully"

# Check if SAM3 is installed
echo ""
echo "Checking SAM3 installation..."
if python3 -c "import sam3" 2>/dev/null; then
    echo "✓ SAM3 is installed"
else
    echo "⚠️  SAM3 is not installed. Installing..."
    pip install -e .
    echo "✓ SAM3 installed"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  cd backend && python main.py"
echo ""
echo "The application will be available at:"
echo "  http://localhost:8000"
echo ""
echo "Note: Models will be downloaded on first use (requires HF_TOKEN)"
echo "Set your Hugging Face token:"
echo "  export HF_TOKEN=your_token_here"
echo ""
