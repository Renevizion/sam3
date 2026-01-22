#!/usr/bin/env python3
"""
Backend startup script for SAM 3 Web Application
Run this from the webapp/backend directory or from the repository root
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import sam3
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

# Change to backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    from main import app
    
    print("=" * 50)
    print("🏭 SAM 3 Factory Monitor - Backend Server")
    print("=" * 50)
    print()
    print("📍 Server will run on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print()
    print("⚠️  Make sure you have:")
    print("   1. Requested SAM 3 weights from Hugging Face")
    print("   2. Authenticated with 'huggingface-cli login'")
    print("   3. A GPU for real-time performance (optional)")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
