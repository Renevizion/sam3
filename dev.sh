#!/bin/bash
# Development server runner - starts both frontend and backend

set -e

echo "🔧 SAM3 Web Application - Development Mode"
echo "==========================================="

# Check if backend dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing backend dependencies..."
    cd backend && pip install -q -r requirements.txt && cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install --silent && cd ..
fi

echo ""
echo "Starting development servers..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

# Determine log directory (prefer local, fallback to /tmp)
LOG_DIR="./logs"
mkdir -p "$LOG_DIR" 2>/dev/null || LOG_DIR="/tmp"

# Start backend in background
echo "🐍 Starting backend server on http://localhost:8000"
cd backend
python main.py > "$LOG_DIR/sam3-backend.log" 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend in background
echo "⚛️  Starting frontend dev server on http://localhost:5173"
cd frontend
npm run dev > "$LOG_DIR/sam3-frontend.log" 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both servers are running!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Logs:"
echo "   Backend:  tail -f $LOG_DIR/sam3-backend.log"
echo "   Frontend: tail -f $LOG_DIR/sam3-frontend.log"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
