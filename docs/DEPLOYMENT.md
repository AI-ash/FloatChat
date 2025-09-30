# FloatChat Deployment Guide 🚀

This guide covers different deployment options for FloatChat, from local development to production cloud deployment.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Git installed
- API keys for required services (see [CLOUD_APIS_SETUP.md](CLOUD_APIS_SETUP.md))

## 🐳 Docker Deployment (Recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/floatchat.git
cd floatchat

# Setup environment
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your API keys:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here

# Optional
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgresql_url_here
REDIS_URL=your_redis_url_here
```

### 3. Deploy

```bash
# Linux/Mac
./deploy.sh

# Windows
deploy.bat
```

### 4. Verify Deployment

The deployment script will automatically check service health. You should see:

```
✅ Backend is healthy
✅ Frontend is healthy
🎉 FloatChat deployed successfully!
```

### 5. Access Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Manual Docker Commands

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f floatchat

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build -d

# Scale services (if needed)
docker-compose up -d --scale floatchat=2
```

## 💻 Local Development

For development without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python run_floatchat.py

# Or run components separately
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
streamlit run frontend/app.py --server.port 8501
```

## ☁️ Cloud Deployment

### Heroku

1. **Create Heroku app**:
   ```bash
   heroku create your-floatchat-app
   ```

2. **Set environment variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_key_here
   heroku config:set COHERE_API_KEY=your_key_here
   heroku config:set PINECONE_API_KEY=your_key_here
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Railway

1. **Connect GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard
3. **Deploy automatically** on git push

### DigitalOcean App Platform

1. **Create new app** from GitHub repository
2. **Configure environment variables**
3. **Set build and run commands**:
   - Build: `pip install -r requirements-production.txt`
   - Run: `python run_floatchat.py`

### AWS ECS / Google Cloud Run

Use the provided `Dockerfile` for container-based deployment:

```bash
# Build image
docker build -t floatchat .

# Tag for registry
docker tag floatchat:latest your-registry/floatchat:latest

# Push to registry
docker push your-registry/floatchat:latest
```

## 🔍 Health Checks & Monitoring

### Built-in Health Checks

- **Backend**: `GET /` returns service status
- **Docker**: Health check every 30 seconds
- **Logs**: Available via `docker-compose logs`

### Monitoring Endpoints

- **Health**: `http://localhost:8000/`
- **Metrics**: `http://localhost:8000/metrics` (if enabled)
- **API Docs**: `http://localhost:8000/docs`

### Log Locations

- **Docker logs**: `docker-compose logs -f`
- **Application logs**: `./logs/` directory (if configured)

## 🛠️ Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using the port
   netstat -ano | findstr :8000
   # Kill the process
   taskkill /f /pid <PID>
   ```

2. **API key errors**:
   - Verify all required API keys are set in `.env`
   - Check API key validity and quotas

3. **Docker build fails**:
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Rebuild without cache
   docker-compose build --no-cache
   ```

4. **Service won't start**:
   ```bash
   # Check logs
   docker-compose logs floatchat
   # Restart services
   docker-compose restart
   ```

### Performance Tuning

1. **Memory limits** (in docker-compose.yml):
   ```yaml
   services:
     floatchat:
       deploy:
         resources:
           limits:
             memory: 1G
   ```

2. **Worker processes** (for production):
   ```bash
   # Use gunicorn for production
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 🔐 Security Considerations

### Production Security

1. **Environment variables**: Never commit `.env` to git
2. **API keys**: Use secrets management in production
3. **HTTPS**: Enable SSL/TLS for production deployments
4. **Firewall**: Restrict access to necessary ports only

### Docker Security

```yaml
# docker-compose.yml security settings
services:
  floatchat:
    user: "1000:1000"  # Non-root user
    read_only: true     # Read-only filesystem
    cap_drop:
      - ALL             # Drop all capabilities
```

## 📊 Scaling

### Horizontal Scaling

```bash
# Scale to multiple instances
docker-compose up -d --scale floatchat=3
```

### Load Balancing

Use nginx or cloud load balancers:

```nginx
upstream floatchat {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}
```

## 🔄 Updates & Maintenance

### Updating FloatChat

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up --build -d

# Verify update
curl http://localhost:8000/
```

### Backup & Recovery

```bash
# Backup configuration
cp .env .env.backup

# Export Docker volumes (if using persistent storage)
docker run --rm -v floatchat_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .
```

## 📞 Support

- **Documentation**: Check other files in `docs/` folder
- **Issues**: Report on GitHub Issues
- **Logs**: Always include logs when reporting issues

---

**Happy Deploying!** 🌊🚀