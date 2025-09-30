<<<<<<< HEAD
#!/usr/bin/env python3
"""
FloatChat startup script with environment validation
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Please copy .env.example to .env and configure your API keys")
        print("📖 See docs/CLOUD_APIS_SETUP.md for detailed setup instructions")
        return False
    
    # Check critical environment variables
    required_vars = [
        "DATABASE_URL",
        "GROQ_API_KEY", 
        "PINECONE_API_KEY",
        "COHERE_API_KEY",
        "REDIS_URL"
    ]
    
    missing_vars = []
    with open(env_file) as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content or f"{var}=\"\"" in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📖 Please see docs/CLOUD_APIS_SETUP.md for setup instructions")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_database():
    """Initialize database tables"""
    print("🗄️ Setting up database...")
    try:
        from backend.database import create_tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("💡 Make sure your DATABASE_URL is correct and the database is accessible")
        return False

def start_services():
    """Start the FloatChat services"""
    print("🚀 Starting FloatChat services...")
    
    try:
        # Start the main application
        from run import FloatChatRunner
        runner = FloatChatRunner()
        runner.run()
        
    except KeyboardInterrupt:
        print("\n👋 FloatChat stopped by user")
    except Exception as e:
        print(f"❌ Error starting services: {e}")

def main():
    """Main startup function"""
    print("🌊 FloatChat - AI-Powered ARGO Data System")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("⚠️ Database setup failed, but continuing...")
        print("💡 You may need to set up your cloud database manually")
    
    # Start services
    start_services()

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
FloatChat startup script with environment validation
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Please copy .env.example to .env and configure your API keys")
        print("📖 See docs/CLOUD_APIS_SETUP.md for detailed setup instructions")
        return False
    
    # Check critical environment variables
    required_vars = [
        "DATABASE_URL",
        "GROQ_API_KEY", 
        "PINECONE_API_KEY",
        "COHERE_API_KEY",
        "REDIS_URL"
    ]
    
    missing_vars = []
    with open(env_file) as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content or f"{var}=\"\"" in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📖 Please see docs/CLOUD_APIS_SETUP.md for setup instructions")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_database():
    """Initialize database tables"""
    print("🗄️ Setting up database...")
    try:
        from backend.database import create_tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("💡 Make sure your DATABASE_URL is correct and the database is accessible")
        return False

def start_services():
    """Start the FloatChat services"""
    print("🚀 Starting FloatChat services...")
    
    try:
        # Start the main application
        from run import FloatChatRunner
        runner = FloatChatRunner()
        runner.run()
        
    except KeyboardInterrupt:
        print("\n👋 FloatChat stopped by user")
    except Exception as e:
        print(f"❌ Error starting services: {e}")

def main():
    """Main startup function"""
    print("🌊 FloatChat - AI-Powered ARGO Data System")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("⚠️ Database setup failed, but continuing...")
        print("💡 You may need to set up your cloud database manually")
    
    # Start services
    start_services()

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    main()