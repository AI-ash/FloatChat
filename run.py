"""
Main runner script for FloatChat application
"""
import asyncio
import subprocess
import sys
import time
import logging
from pathlib import Path
import signal
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FloatChatRunner:
    """Main application runner"""
    
    def __init__(self):
        self.processes = []
        self.running = True
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Received shutdown signal, stopping services...")
        self.running = False
        self.stop_all_processes()
        sys.exit(0)
    
    def start_backend(self):
        """Start the FastAPI backend"""
        try:
            logger.info("Starting FastAPI backend...")
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn",
                "backend.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ])
            self.processes.append(("backend", process))
            return process
        except Exception as e:
            logger.error(f"Error starting backend: {e}")
            return None
    
    def start_frontend(self):
        """Start the Streamlit frontend"""
        try:
            logger.info("Starting Streamlit frontend...")
            process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run",
                "frontend/app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0"
            ])
            self.processes.append(("frontend", process))
            return process
        except Exception as e:
            logger.error(f"Error starting frontend: {e}")
            return None
    
    def start_data_ingestion(self):
        """Start periodic data ingestion"""
        try:
            logger.info("Starting data ingestion service...")
            process = subprocess.Popen([
                sys.executable, "-c",
                """
import asyncio
import time
from data.ingestion.argo_ingester import run_ingestion

async def periodic_ingestion():
    while True:
        try:
            await run_ingestion()
            print("Data ingestion completed, sleeping for 1 hour...")
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            print(f"Ingestion error: {e}")
            await asyncio.sleep(300)  # Retry after 5 minutes

if __name__ == "__main__":
    asyncio.run(periodic_ingestion())
                """
            ])
            self.processes.append(("ingestion", process))
            return process
        except Exception as e:
            logger.error(f"Error starting data ingestion: {e}")
            return None
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        try:
            # Check if Ollama is running
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                logger.warning("Ollama is not running. Please start Ollama first.")
                logger.info("Install Ollama from: https://ollama.ai")
                logger.info("Then run: ollama pull llama3")
                return False
        except Exception:
            logger.warning("Ollama is not accessible. Some AI features may not work.")
        
        # Check database connection
        try:
            from backend.database import engine
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            logger.info("Database connection successful")
        except Exception as e:
            logger.warning(f"Database connection failed: {e}")
            logger.info("Please ensure PostgreSQL is running and configured correctly")
        
        return True
    
    def setup_database(self):
        """Setup database tables"""
        try:
            logger.info("Setting up database tables...")
            from backend.database import create_tables
            create_tables()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error setting up database: {e}")
    
    def stop_all_processes(self):
        """Stop all running processes"""
        for name, process in self.processes:
            try:
                logger.info(f"Stopping {name}...")
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {name}...")
                process.kill()
            except Exception as e:
                logger.error(f"Error stopping {name}: {e}")
    
    def run(self, mode="full"):
        """Run the application"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("Starting FloatChat application...")
        
        # Check dependencies
        if not self.check_dependencies():
            logger.warning("Some dependencies are missing, but continuing...")
        
        # Setup database
        self.setup_database()
        
        # Start services based on mode
        if mode in ["full", "backend"]:
            backend_process = self.start_backend()
            if not backend_process:
                logger.error("Failed to start backend")
                return
        
        if mode in ["full", "frontend"]:
            # Wait a bit for backend to start
            if mode == "full":
                time.sleep(3)
            
            frontend_process = self.start_frontend()
            if not frontend_process:
                logger.error("Failed to start frontend")
                return
        
        if mode in ["full", "ingestion"]:
            ingestion_process = self.start_data_ingestion()
            if not ingestion_process:
                logger.warning("Failed to start data ingestion")
        
        # Print startup information
        logger.info("=" * 60)
        logger.info("FloatChat is starting up!")
        logger.info("=" * 60)
        
        if mode in ["full", "backend"]:
            logger.info("🔧 Backend API: http://localhost:8000")
            logger.info("📚 API Docs: http://localhost:8000/docs")
        
        if mode in ["full", "frontend"]:
            logger.info("🌊 Frontend App: http://localhost:8501")
        
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop all services")
        logger.info("=" * 60)
        
        # Keep running and monitor processes
        try:
            while self.running:
                time.sleep(1)
                
                # Check if any process has died
                for name, process in self.processes[:]:
                    if process.poll() is not None:
                        logger.warning(f"{name} process has stopped")
                        self.processes.remove((name, process))
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            self.stop_all_processes()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FloatChat Application Runner")
    parser.add_argument(
        "--mode",
        choices=["full", "backend", "frontend", "ingestion"],
        default="full",
        help="Which services to run"
    )
    
    args = parser.parse_args()
    
    runner = FloatChatRunner()
    runner.run(mode=args.mode)

if __name__ == "__main__":
    main()