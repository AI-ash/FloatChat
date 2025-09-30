<<<<<<< HEAD
#!/usr/bin/env python3
"""
Simple FloatChat Startup Script
Starts the application without complex database setup
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FloatChat Backend...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])
    return backend_process

def start_frontend():
    """Start the Streamlit frontend"""
    print("🌊 Starting FloatChat Frontend...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    return frontend_process

def main():
    print("🌊 FloatChat - Simple Startup")
    print("=" * 50)
    
    try:
        # Start backend
        backend = start_backend()
        time.sleep(3)
        
        # Start frontend
        frontend = start_frontend()
        time.sleep(5)
        
        print("\n" + "=" * 50)
        print("✅ FloatChat is running!")
        print("=" * 50)
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("🌊 Frontend App: http://localhost:8501")
        print("=" * 50)
        print("Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        # Wait for processes
        try:
            backend.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            backend.terminate()
            frontend.terminate()
            print("✅ Services stopped")
            
    except Exception as e:
        print(f"❌ Error starting FloatChat: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Simple FloatChat Startup Script
Starts the application without complex database setup
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FloatChat Backend...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])
    return backend_process

def start_frontend():
    """Start the Streamlit frontend"""
    print("🌊 Starting FloatChat Frontend...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    return frontend_process

def main():
    print("🌊 FloatChat - Simple Startup")
    print("=" * 50)
    
    try:
        # Start backend
        backend = start_backend()
        time.sleep(3)
        
        # Start frontend
        frontend = start_frontend()
        time.sleep(5)
        
        print("\n" + "=" * 50)
        print("✅ FloatChat is running!")
        print("=" * 50)
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("🌊 Frontend App: http://localhost:8501")
        print("=" * 50)
        print("Press Ctrl+C to stop all services")
        print("=" * 50)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        # Wait for processes
        try:
            backend.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            backend.terminate()
            frontend.terminate()
            print("✅ Services stopped")
            
    except Exception as e:
        print(f"❌ Error starting FloatChat: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    sys.exit(main())