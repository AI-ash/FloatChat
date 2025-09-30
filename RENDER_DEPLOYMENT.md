# 🚀 FloatChat Render Deployment Guide

This guide will help you deploy FloatChat to Render.com using Docker.

## 📋 Prerequisites

1. **GitHub Repository**: Your FloatChat code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **API Keys**: Get the following API keys (all have free tiers):
   - [Groq API Key](https://console.groq.com) - For fast LLM inference
   - [Cohere API Key](https://cohere.com) - For embeddings
   - [Pinecone API Key](https://pinecone.io) - For vector database
   - [OpenAI API Key](https://platform.openai.com) - Optional backup

## 🔧 Pre-Deployment Setup

### 1. Verify Your Repository Structure

Ensure your repository has these files:
```
floatchat/
├── Dockerfile                 # ✅ Optimized for Render
├── render.yaml               # ✅ Render configuration
├── requirements-production.txt # ✅ Production dependencies
├── start_streamlit.py        # ✅ Main entry point
├── streamlit_app.py          # ✅ Streamlit application
├── backend/                  # ✅ FastAPI backend
├── frontend/                 # ✅ Streamlit frontend
├── .dockerignore            # ✅ Optimized Docker build
└── .env.example             # ✅ Environment template
```

### 2. Test Locally (Optional but Recommended)

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/floatchat.git
cd floatchat

# Create environment file
cp .env.example .env
# Edit .env with your API keys

# Test Docker build
docker build -t floatchat .
docker run -p 10000:10000 --env-file .env floatchat
```

## 🌐 Deploy to Render

### Step 1: Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `floatchat` repository

### Step 2: Configure Service Settings

**Basic Settings:**
- **Name**: `floatchat` (or your preferred name)
- **Environment**: `Docker`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (uses repository root)

**Advanced Settings:**
- **Dockerfile Path**: `./Dockerfile`
- **Docker Context**: `.`
- **Plan**: `Free` (for testing) or `Starter` (for production)

### Step 3: Environment Variables

Add these environment variables in the Render dashboard:

**Required (Core Functionality):**
```
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

**Optional (Enhanced Features):**
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgresql_url_here
REDIS_URL=your_redis_url_here
```

**Application Settings:**
```
APP_NAME=FloatChat
APP_VERSION=1.0.0
DEBUG=false
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=floatchat-knowledge
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Build the Docker image
   - Deploy the service
3. Wait for deployment to complete (5-10 minutes)

## 🔍 Post-Deployment Verification

### 1. Check Deployment Status

- Go to your service dashboard
- Verify the deployment status is **"Live"**
- Check the logs for any errors

### 2. Test Your Application

1. **Access the Application**: Visit your Render URL (e.g., `https://floatchat.onrender.com`)
2. **Test Core Features**:
   - Load the Streamlit interface
   - Try a sample query: "Show me temperature data in Bay of Bengal"
   - Verify visualizations display correctly
   - Check that the backend API responds

### 3. Monitor Logs

- Go to **"Logs"** tab in your Render dashboard
- Look for:
  - ✅ "Starting FloatChat on port XXXX"
  - ✅ "Starting FastAPI backend on port XXXX"
  - ✅ "Connected to backend: http://localhost:XXXX"
  - ❌ Any error messages

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures

**Problem**: Docker build fails
**Solutions**:
- Check `requirements-production.txt` for version conflicts
- Verify all dependencies are available
- Check Dockerfile syntax

#### 2. Application Won't Start

**Problem**: Service shows "Failed" status
**Solutions**:
- Check environment variables are set correctly
- Verify API keys are valid
- Check logs for specific error messages

#### 3. Timeout Errors

**Problem**: Application times out during startup
**Solutions**:
- Increase startup timeout in Render settings
- Optimize application startup time
- Check for blocking operations during startup

#### 4. API Connection Issues

**Problem**: Frontend can't connect to backend
**Solutions**:
- Verify `BACKEND_PORT` environment variable
- Check that both services start correctly
- Review network configuration

### Debug Commands

If you need to debug locally:

```bash
# Test with same environment as Render
docker run -p 10000:10000 \
  -e GROQ_API_KEY=your_key \
  -e COHERE_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  floatchat

# Check logs
docker logs <container_id>

# Test API endpoints
curl http://localhost:10000/
curl http://localhost:8000/
```

## 📊 Performance Optimization

### For Production Deployment

1. **Upgrade Plan**: Use "Starter" or higher plan for better performance
2. **Environment Variables**: Set `DEBUG=false` for production
3. **Caching**: Enable Redis for better performance
4. **Database**: Use PostgreSQL for persistent data storage

### Monitoring

- **Uptime**: Monitor service availability
- **Response Times**: Track API response times
- **Error Rates**: Monitor error logs
- **Resource Usage**: Check CPU and memory usage

## 🔄 Updates and Maintenance

### Updating Your Application

1. **Push Changes**: Commit and push changes to your GitHub repository
2. **Auto-Deploy**: Render automatically redeploys on push to main branch
3. **Manual Deploy**: Use "Manual Deploy" button for specific commits

### Environment Variable Updates

1. Go to **"Environment"** tab
2. Add/update environment variables
3. Click **"Save Changes"**
4. Service will automatically restart

## 💰 Cost Management

### Free Tier Limits

- **750 hours/month** of service time
- **512 MB RAM**
- **0.1 CPU**
- **Sleeps after 15 minutes** of inactivity

### Upgrading Plans

- **Starter**: $7/month - Always on, 512 MB RAM
- **Standard**: $25/month - Always on, 1 GB RAM
- **Pro**: $85/month - Always on, 2 GB RAM

## 🎉 Success Checklist

Your deployment is successful when:

- ✅ Service shows "Live" status
- ✅ Application loads without errors
- ✅ Natural language queries work
- ✅ Visualizations display correctly
- ✅ No critical errors in logs
- ✅ Response times are acceptable (< 15 seconds)

## 📞 Support

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)

### FloatChat Support
- Check logs for specific error messages
- Review this deployment guide
- Test locally with Docker first

## 🎯 Next Steps

After successful deployment:

1. **Share Your App**: Get your public URL from Render dashboard
2. **Monitor Usage**: Track user interactions and performance
3. **Scale Up**: Upgrade plan if needed for more users
4. **Add Features**: Continue developing new features
5. **Backup**: Set up regular backups of your data

---

## 🚀 Quick Deploy Commands

If you prefer command-line deployment:

```bash
# Install Render CLI
npm install -g @render/cli

# Login to Render
render login

# Deploy from local directory
render deploy

# Or deploy specific service
render services create --name floatchat --type web --dockerfile ./Dockerfile
```

**Congratulations! Your FloatChat application is now live on Render! 🌊🚀**
