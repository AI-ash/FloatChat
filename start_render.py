#!/usr/bin/env python3
"""
Render.com startup script for FloatChat Docker deployment
"""

import subprocess
import sys
import os
import time
import signal
import threading

def start_backend():
    """Start the FastAPI backend"""
    port = os.getenv('PORT', '10000')
    print(f"🚀 Starting Backend on port {port}...")
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", port,
        "--workers", "1"
    ]
    
    return subprocess.Popen(cmd)

def start_frontend():
    """Start the Streamlit frontend on a different port"""
    main_port = int(os.getenv('PORT', '10000'))
    frontend_port = main_port + 1
    
    print(f"🌊 Starting Frontend on port {frontend_port}...")
    
    # Set backend URL to the main port
    os.environ['BACKEND_URL'] = f"http://localhost:{main_port}"
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/app.py",
        "--server.port", str(frontend_port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    return subprocess.Popen(cmd)

def create_nginx_config():
    """Create nginx config to proxy frontend through main port"""
    nginx_config = f"""
events {{
    worker_connections 1024;
}}

http {{
    upstream backend {{
        server localhost:{os.getenv('PORT', '10000')};
    }}
    
    upstream frontend {{
        server localhost:{int(os.getenv('PORT', '10000')) + 1};
    }}
    
    server {{
        listen 8080;
        
        location /api/ {{
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }}
        
        location / {{
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }}
    }}
}}
"""
    
    with open('/tmp/nginx.conf', 'w') as f:
        f.write(nginx_config)

def main():
    """Main function for Render Docker deployment"""
    print("🌊 FloatChat - Render Docker Deployment")
    print("=" * 50)
    
    port = os.getenv('PORT', '10000')
    print(f"🔧 Main port: {port}")
    
    # For Render, we'll run backend on the main port
    # and let users access it directly for API calls
    print("🚀 Starting backend service...")
    backend_process = start_backend()
    
    # Wait for backend to start
    time.sleep(10)
    
    print("✅ FloatChat Backend is running!")
    print("=" * 50)
    print(f"🔧 Backend API: Port {port}")
    print(f"📚 API Docs: /docs")
    print(f"🌊 Health Check: /")
    print("=" * 50)
    
    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down...")
        backend_process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Keep the backend running
        backend_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()