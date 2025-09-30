#!/usr/bin/env python3
"""
Render deployment with Streamlit frontend and FastAPI backend
"""

import os
import sys
import subprocess
import threading
import time
import signal

def start_backend():
    """Start FastAPI backend on internal port"""
    backend_port = int(os.getenv('PORT', '10000')) + 1000
    print(f"🚀 Starting Backend on internal port {backend_port}")
    
    # Set environment variable for backend
    os.environ['BACKEND_PORT'] = str(backend_port)
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", str(backend_port),
        "--workers", "1"
    ]
    
    return subprocess.Popen(cmd)

def start_frontend():
    """Start Streamlit frontend on main port"""
    frontend_port = int(os.getenv('PORT', '10000'))
    backend_port = int(os.getenv('PORT', '10000')) + 1000
    
    print(f"🌊 Starting Streamlit Frontend on port {frontend_port}")
    
    # Set backend URL for frontend
    os.environ['BACKEND_URL'] = f"http://localhost:{backend_port}"
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", str(frontend_port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    return subprocess.Popen(cmd)

def main():
    """Main function for Render deployment"""
    print("🌊 FloatChat - Streamlit + FastAPI on Render")
    print("=" * 50)
    
    main_port = int(os.getenv('PORT', '10000'))
    backend_port = main_port + 1000
    
    print(f"🌊 Frontend (Streamlit): Port {main_port} (Public)")
    print(f"🔧 Backend (FastAPI): Port {backend_port} (Internal)")
    
    # Start backend first
    print("Starting backend...")
    backend_process = start_backend()
    time.sleep(8)  # Wait for backend to start
    
    # Start frontend
    print("Starting frontend...")
    frontend_process = start_frontend()
    
    print("\n" + "=" * 50)
    print("✅ FloatChat is running!")
    print(f"🌊 Streamlit UI: Port {main_port}")
    print(f"🔧 FastAPI Backend: Port {backend_port}")
    print("=" * 50)
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down...")
        try:
            backend_process.terminate()
            frontend_process.terminate()
        except:
            pass
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Keep both processes running
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend died, restarting...")
                backend_process = start_backend()
                time.sleep(5)
            
            if frontend_process.poll() is not None:
                print("❌ Frontend died, restarting...")
                frontend_process = start_frontend()
                time.sleep(5)
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()