#!/usr/bin/env python3
"""
Streamlit startup for Render deployment
Handles both Streamlit frontend and embedded FastAPI backend
"""

import os
import sys
import subprocess
import threading
import time
import signal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_fastapi_backend():
    """Start FastAPI backend in background thread"""
    try:
        import uvicorn
        from backend.main import app
        
        backend_port = int(os.getenv('BACKEND_PORT', '8000'))
        logger.info(f"🚀 Starting FastAPI backend on port {backend_port}")
        
        # Configure uvicorn for production
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=backend_port,
            log_level="warning",
            access_log=False,
            workers=1,  # Single worker for Render
            loop="asyncio"
        )
        
        server = uvicorn.Server(config)
        server.run()
        
    except Exception as e:
        logger.error(f"Failed to start FastAPI backend: {e}")
        # Try alternative configuration
        try:
            logger.info("🔄 Trying alternative backend configuration...")
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=backend_port,
                log_level="error",
                access_log=False,
                reload=False
            )
        except Exception as e2:
            logger.error(f"Alternative backend startup also failed: {e2}")

def main():
    """Start Streamlit app with embedded backend"""
    # Get port from Render environment
    port = int(os.getenv('PORT', '10000'))
    backend_port = int(os.getenv('BACKEND_PORT', '8000'))
    
    logger.info(f"🌊 Starting FloatChat on port {port}")
    logger.info(f"🔧 Backend will run on port {backend_port}")
    
    # Set environment variables for the app
    os.environ['BACKEND_URL'] = f"http://localhost:{backend_port}"
    
    # Start FastAPI backend in background thread
    backend_thread = threading.Thread(target=start_fastapi_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    # Streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "streamlit_app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false",
        "--server.runOnSave", "false"
    ]
    
    logger.info(f"🎯 Starting Streamlit with command: {' '.join(cmd)}")
    
    try:
        # Run Streamlit
        subprocess.run(cmd)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down FloatChat...")
    except Exception as e:
        logger.error(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()