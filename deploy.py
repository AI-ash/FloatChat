#!/usr/bin/env python3
"""
FloatChat Cloud Deployment Script
Automates the deployment process to various cloud platforms
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

class CloudDeployer:
    """Handles deployment to various cloud platforms"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / ".env"
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check if .env file exists
        if not self.env_file.exists():
            print("❌ .env file not found. Please copy .env.example to .env and fill in your API keys.")
            return False
        
        # Check if required API keys are set
        required_keys = [
            "DATABASE_URL",
            "GROQ_API_KEY",
            "PINECONE_API_KEY",
            "COHERE_API_KEY"
        ]
        
        missing_keys = []
        with open(self.env_file) as f:
            env_content = f.read()
            for key in required_keys:
                if f"{key}=" not in env_content or f"{key}=your_" in env_content:
                    missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Missing API keys: {', '.join(missing_keys)}")
            print("📖 Please see docs/CLOUD_APIS_SETUP.md for setup instructions")
            return False
        
        print("✅ Prerequisites check passed!")
        return True
    
    def deploy_to_vercel(self):
        """Deploy frontend to Vercel"""
        print("🚀 Deploying to Vercel...")
        
        # Create vercel.json configuration
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "frontend/app.py",
                    "use": "@vercel/python"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "frontend/app.py"
                }
            ],
            "env": {
                "BACKEND_URL": "https://your-backend-url.railway.app"
            }
        }
        
        with open("vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        
        try:
            subprocess.run(["vercel", "--prod"], check=True)
            print("✅ Successfully deployed to Vercel!")
        except subprocess.CalledProcessError:
            print("❌ Vercel deployment failed. Make sure Vercel CLI is installed.")
            print("Install: npm i -g vercel")
        except FileNotFoundError:
            print("❌ Vercel CLI not found. Install with: npm i -g vercel")
    
    def deploy_to_railway(self):
        """Deploy backend to Railway"""
        print("🚀 Deploying to Railway...")
        
        # Create railway.json configuration
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                "healthcheckPath": "/",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        with open("railway.json", "w") as f:
            json.dump(railway_config, f, indent=2)
        
        print("📝 Railway configuration created.")
        print("🔗 Please connect your GitHub repository to Railway dashboard:")
        print("   1. Go to https://railway.app")
        print("   2. Create new project from GitHub repo")
        print("   3. Add environment variables from your .env file")
        print("   4. Deploy!")
    
    def deploy_to_heroku(self):
        """Deploy to Heroku"""
        print("🚀 Deploying to Heroku...")
        
        # Create Procfile
        procfile_content = """
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
worker: python data/ingestion/argo_ingester.py
"""
        
        with open("Procfile", "w") as f:
            f.write(procfile_content.strip())
        
        # Create runtime.txt
        with open("runtime.txt", "w") as f:
            f.write("python-3.11.0")
        
        try:
            # Initialize git if not already
            if not (self.project_root / ".git").exists():
                subprocess.run(["git", "init"], check=True)
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            
            # Create Heroku app
            app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
            if app_name:
                subprocess.run(["heroku", "create", app_name], check=True)
            else:
                subprocess.run(["heroku", "create"], check=True)
            
            # Set environment variables (excluding sensitive ones)
            print("📝 Setting environment variables...")
            with open(self.env_file) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        # Skip setting example/placeholder values
                        if not value.startswith("your-") and value != "":
                            subprocess.run(["heroku", "config:set", f"{key}={value}"], check=True)
            
            # Deploy
            subprocess.run(["git", "push", "heroku", "main"], check=True)
            print("✅ Successfully deployed to Heroku!")
            
        except subprocess.CalledProcessError:
            print("❌ Heroku deployment failed. Make sure Heroku CLI is installed.")
        except FileNotFoundError:
            print("❌ Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli")
    
    def deploy_to_digitalocean(self):
        """Deploy to DigitalOcean App Platform"""
        print("🚀 Preparing DigitalOcean App Platform deployment...")
        
        # Create .do/app.yaml configuration
        os.makedirs(".do", exist_ok=True)
        
        do_config = {
            "name": "floatchat",
            "services": [
                {
                    "name": "backend",
                    "source_dir": "/",
                    "github": {
                        "repo": "your-username/floatchat",
                        "branch": "main"
                    },
                    "run_command": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
                    "environment_slug": "python",
                    "instance_count": 1,
                    "instance_size_slug": "basic-xxs",
                    "http_port": 8000,
                    "routes": [
                        {
                            "path": "/api"
                        }
                    ]
                },
                {
                    "name": "frontend",
                    "source_dir": "/",
                    "github": {
                        "repo": "your-username/floatchat",
                        "branch": "main"
                    },
                    "run_command": "streamlit run frontend/app.py --server.port $PORT",
                    "environment_slug": "python",
                    "instance_count": 1,
                    "instance_size_slug": "basic-xxs",
                    "http_port": 8501,
                    "routes": [
                        {
                            "path": "/"
                        }
                    ]
                }
            ]
        }
        
        with open(".do/app.yaml", "w") as f:
            import yaml
            yaml.dump(do_config, f, default_flow_style=False)
        
        print("📝 DigitalOcean configuration created at .do/app.yaml")
        print("🔗 Please deploy using DigitalOcean dashboard:")
        print("   1. Go to https://cloud.digitalocean.com/apps")
        print("   2. Create app from GitHub repository")
        print("   3. Use the generated .do/app.yaml configuration")
        print("   4. Add environment variables from your .env file")
    
    def create_docker_files(self):
        """Create Docker files for containerized deployment"""
        print("🐳 Creating Docker configuration files...")
        
        # Dockerfile for backend
        backend_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        with open("Dockerfile.backend", "w") as f:
            f.write(backend_dockerfile.strip())
        
        # Dockerfile for frontend
        frontend_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
"""
        
        with open("Dockerfile.frontend", "w") as f:
            f.write(frontend_dockerfile.strip())
        
        # Dockerfile for ingestion
        ingestion_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-c", "import asyncio; from data.ingestion.argo_ingester import run_ingestion; asyncio.run(run_ingestion())"]
"""
        
        with open("Dockerfile.ingestion", "w") as f:
            f.write(ingestion_dockerfile.strip())
        
        print("✅ Docker files created successfully!")
        print("🚀 You can now deploy using: docker-compose up -d")

def main():
    parser = argparse.ArgumentParser(description="Deploy FloatChat to cloud platforms")
    parser.add_argument(
        "platform",
        choices=["vercel", "railway", "heroku", "digitalocean", "docker"],
        help="Target deployment platform"
    )
    
    args = parser.parse_args()
    
    deployer = CloudDeployer()
    
    # Check prerequisites
    if not deployer.check_prerequisites():
        sys.exit(1)
    
    # Deploy to selected platform
    if args.platform == "vercel":
        deployer.deploy_to_vercel()
    elif args.platform == "railway":
        deployer.deploy_to_railway()
    elif args.platform == "heroku":
        deployer.deploy_to_heroku()
    elif args.platform == "digitalocean":
        deployer.deploy_to_digitalocean()
    elif args.platform == "docker":
        deployer.create_docker_files()
    
    print("\n🎉 Deployment preparation complete!")
    print("📖 For detailed setup instructions, see docs/CLOUD_APIS_SETUP.md")

if __name__ == "__main__":
    main()