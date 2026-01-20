#!/bin/bash

# SAM 3 Web Application Startup Script
# This script helps start both backend and frontend servers

set -e

echo "🏭 SAM 3 Factory Monitor - Startup Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "webapp" ]; then
    echo "❌ Error: webapp directory not found"
    echo "Please run this script from the sam3 repository root"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo "❌ Error: Node.js is not installed"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"
echo "✅ Node.js version: $(node --version)"
echo ""

# Check if backend dependencies are installed
echo "📦 Checking backend dependencies..."
if [ ! -f "webapp/backend/requirements.txt" ]; then
    echo "❌ Error: Backend requirements.txt not found"
    exit 1
fi

# Check if frontend dependencies are installed
echo "📦 Checking frontend dependencies..."
if [ ! -d "webapp/frontend/node_modules" ]; then
    echo "⚠️  Frontend dependencies not installed"
    echo "Installing frontend dependencies..."
    cd webapp/frontend
    npm install
    cd ../..
    echo "✅ Frontend dependencies installed"
else
    echo "✅ Frontend dependencies already installed"
fi

echo ""
echo "🚀 Starting servers..."
echo ""

# Create logs directory if it doesn't exist
mkdir -p webapp/logs

# Clean up old logs (keep last 5 days)
find webapp/logs -name "*.log" -mtime +5 -delete 2>/dev/null || true

# Generate timestamp for log files
LOG_TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Start backend in background
echo "Starting backend server on http://localhost:8000"
cd webapp/backend
python3 run.py > ../logs/backend_${LOG_TIMESTAMP}.log 2>&1 &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check webapp/logs/backend_${LOG_TIMESTAMP}.log for errors"
    exit 1
fi

echo "✅ Backend started (PID: $BACKEND_PID)"

# Start frontend in background
echo "Starting frontend server on http://localhost:5173"
cd webapp/frontend
npm run dev > ../logs/frontend_${LOG_TIMESTAMP}.log 2>&1 &
FRONTEND_PID=$!
cd ../..

# Wait a moment for frontend to start
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start. Check webapp/logs/frontend_${LOG_TIMESTAMP}.log for errors"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo ""
echo "=========================================="
echo "🎉 All servers are running!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔌 Backend:  http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "=========================================="

# Trap Ctrl+C and cleanup
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Servers stopped'; exit 0" INT TERM

# Wait for processes
wait
