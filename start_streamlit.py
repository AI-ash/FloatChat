#!/usr/bin/env python3
"""
Simple Streamlit startup for Render
"""

import os
import sys
import subprocess

def main():
    """Start Streamlit app"""
    port = int(os.getenv('PORT', '10000'))
    
    print(f"🌊 Starting FloatChat Streamlit on port {port}")
    
    # Set backend port for internal FastAPI
    os.environ['BACKEND_PORT'] = str(port + 1000)
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    # Run Streamlit
    subprocess.run(cmd)

if __name__ == "__main__":
    main()