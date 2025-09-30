#!/usr/bin/env python3
"""
Cloud deployment startup script for FloatChat
Runs both backend and frontend on cloud platforms
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FloatChat Backend...")
    
    # Get port from environment (for cloud platforms)
    port = os.getenv('PORT', '8000')
    
    # Start backend
    backend_cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", port
    ]
    
    return subprocess.Popen(backend_cmd)

def start_frontend():
    """Start the Streamlit frontend"""
    print("🌊 Starting FloatChat Frontend...")
    
    # Get frontend port (different from backend)
    frontend_port = os.getenv('FRONTEND_PORT', '8501')
    
    # Start frontend
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", frontend_port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false"
    ]
    
    return subprocess.Popen(frontend_cmd)

def main():
    """Main startup function"""
    print("🌊 FloatChat Cloud Startup")
    print("=" * 40)
    
    # Detect cloud platform
    platform = "Unknown"
    if os.getenv('RENDER'):
        platform = "Render"
    elif os.getenv('DYNO'):
        platform = "Heroku"
    elif os.getenv('RAILWAY_ENVIRONMENT'):
        platform = "Railway"
    
    print(f"🌐 Detected platform: {platform}")
    
    # For cloud platforms, we might need to run only one service
    # depending on how the platform is configured
    
    if os.getenv('SERVICE_TYPE') == 'backend':
        # Run only backend
        print("🔧 Starting backend service only...")
        backend_process = start_backend()
        backend_process.wait()
        
    elif os.getenv('SERVICE_TYPE') == 'frontend':
        # Run only frontend
        print("🌊 Starting frontend service only...")
        frontend_process = start_frontend()
        frontend_process.wait()
        
    else:
        # Run both services (default)
        print("🚀 Starting both backend and frontend...")
        
        # Start backend first
        backend_process = start_backend()
        time.sleep(5)  # Wait for backend to start
        
        # Start frontend
        frontend_process = start_frontend()
        
        print("\n" + "=" * 40)
        print("✅ FloatChat is running!")
        print("=" * 40)
        
        port = os.getenv('PORT', '8000')
        frontend_port = os.getenv('FRONTEND_PORT', '8501')
        
        print(f"🔧 Backend: Port {port}")
        print(f"🌊 Frontend: Port {frontend_port}")
        print("=" * 40)
        
        try:
            # Wait for both processes
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            backend_process.terminate()
            frontend_process.terminate()

if __name__ == "__main__":
    main()