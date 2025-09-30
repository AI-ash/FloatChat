<<<<<<< HEAD
#!/usr/bin/env python3
"""
Simple FloatChat runner with proper cleanup
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def start_services():
    """Start FloatChat services"""
    
    print("🌊 FloatChat - Starting Services")
    print("=" * 50)
    
    # Start backend
    print("🚀 Starting Backend API...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])
    
    time.sleep(3)
    
    # Start frontend
    print("🌊 Starting Frontend...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    
    time.sleep(5)
    
    print("\n" + "=" * 50)
    print("✅ FloatChat is running!")
    print("=" * 50)
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🌊 Frontend App: http://localhost:8501")
    print("=" * 50)
    print("📊 Features:")
    print("  • Real oceanographic data from Marine APIs")
    print("  • AI-powered natural language queries")
    print("  • Interactive visualizations")
    print("  • ARGO float data analysis")
    print("=" * 50)
    print("Press Ctrl+C to stop all services")
    print("=" * 50)
    
    def signal_handler(sig, frame):
        print("\n🛑 Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Services stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Wait for processes
        backend_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Simple FloatChat runner with proper cleanup
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def start_services():
    """Start FloatChat services"""
    
    print("🌊 FloatChat - Starting Services")
    print("=" * 50)
    
    # Start backend
    print("🚀 Starting Backend API...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])
    
    time.sleep(3)
    
    # Start frontend
    print("🌊 Starting Frontend...")
    frontend_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    
    time.sleep(5)
    
    print("\n" + "=" * 50)
    print("✅ FloatChat is running!")
    print("=" * 50)
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🌊 Frontend App: http://localhost:8501")
    print("=" * 50)
    print("📊 Features:")
    print("  • Real oceanographic data from Marine APIs")
    print("  • AI-powered natural language queries")
    print("  • Interactive visualizations")
    print("  • ARGO float data analysis")
    print("=" * 50)
    print("Press Ctrl+C to stop all services")
    print("=" * 50)
    
    def signal_handler(sig, frame):
        print("\n🛑 Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Services stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Wait for processes
        backend_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    start_services()