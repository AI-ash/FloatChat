# 🚀 GitHub Deployment Guide for FloatChat

This guide will help you deploy FloatChat to GitHub and set up automatic deployment.

## 📋 Prerequisites

- GitHub account
- Git installed on your computer
- FloatChat project ready for deployment

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
cd /path/to/your/floatchat/project
git init
```

### 1.2 Add all files to Git

```bash
# Add all files except those in .gitignore
git add .

# Commit the files
git commit -m "Initial commit: FloatChat AI-Powered ARGO Data System"
```

## 🌐 Step 2: Create GitHub Repository

### 2.1 Create Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon in the top right
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `floatchat`
   - **Description**: `AI-Powered ARGO Data System for Oceanographic Analysis`
   - **Visibility**: Public (recommended) or Private
   - **Don't** initialize with README (we already have one)

### 2.2 Connect Local Repository to GitHub

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR_USERNAME/floatchat.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 🔐 Step 3: Set Up Secrets

### 3.1 Add Repository Secrets

1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add these secrets one by one:

```
GROQ_API_KEY = your_groq_api_key_here
COHERE_API_KEY = your_cohere_api_key_here
PINECONE_API_KEY = your_pinecone_api_key_here
OPENAI_API_KEY = your_openai_api_key_here (optional)
DATABASE_URL = your_database_url_here (optional)
REDIS_URL = your_redis_url_here (optional)
```

## 🚀 Step 4: Automatic Deployment Options

### Option A: Heroku Deployment

1. **Create Heroku account** at [heroku.com](https://heroku.com)

2. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create your-floatchat-app
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_key_here
   heroku config:set COHERE_API_KEY=your_key_here
   heroku config:set PINECONE_API_KEY=your_key_here
   ```

5. **Create Procfile**:
   ```bash
   echo "web: python run_floatchat.py" > Procfile
   git add Procfile
   git commit -m "Add Procfile for Heroku"
   ```

6. **Deploy**:
   ```bash
   git push heroku main
   ```

### Option B: Railway Deployment

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `floatchat` repository
5. Add environment variables in Railway dashboard
6. Deploy automatically!

### Option C: Render Deployment

1. Go to [Render.com](https://render.com)
2. Connect your GitHub account
3. Create new "Web Service"
4. Select your `floatchat` repository
5. Configure:
   - **Build Command**: `pip install -r requirements-production.txt`
   - **Start Command**: `python run_floatchat.py`
6. Add environment variables
7. Deploy!

## 🔄 Step 5: Set Up Continuous Deployment

### 5.1 GitHub Actions (Already configured!)

The repository includes `.github/workflows/ci.yml` which automatically:
- Tests code on every push
- Builds Docker image
- Runs health checks
- Deploys on main branch updates

### 5.2 Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Enable workflows if prompted
4. Push a change to trigger the first workflow

## 📊 Step 6: Monitor Deployment

### 6.1 Check GitHub Actions

- Go to **Actions** tab in your repository
- Monitor build and deployment status
- Check logs if any step fails

### 6.2 Verify Deployment

Once deployed, test your application:

```bash
# Test the deployed API (replace with your URL)
curl https://your-app-name.herokuapp.com/
curl https://your-app-name.railway.app/
curl https://your-app-name.onrender.com/
```

## 🛠️ Step 7: Custom Domain (Optional)

### 7.1 For Heroku

```bash
heroku domains:add www.your-domain.com
```

### 7.2 For Railway/Render

1. Go to your app dashboard
2. Find "Custom Domain" settings
3. Add your domain
4. Update DNS records as instructed

## 🔧 Step 8: Environment-Specific Configuration

### 8.1 Create environment-specific files

```bash
# Create production environment file
cp .env.example .env.production

# Edit with production values
# Note: Don't commit this file!
```

### 8.2 Update deployment scripts

Modify `deploy.sh` or `deploy.bat` for production:

```bash
# Use production environment
export NODE_ENV=production
export DEBUG=false
```

## 📈 Step 9: Monitoring & Maintenance

### 9.1 Set up monitoring

1. **Application monitoring**: Use services like Sentry, LogRocket
2. **Uptime monitoring**: Use UptimeRobot, Pingdom
3. **Performance monitoring**: Use New Relic, DataDog

### 9.2 Regular maintenance

```bash
# Update dependencies regularly
pip list --outdated
pip install -r requirements.txt --upgrade

# Update Docker images
docker pull python:3.9-slim
docker-compose build --no-cache
```

## 🆘 Troubleshooting

### Common Issues

1. **Build fails on GitHub Actions**:
   - Check if all secrets are set correctly
   - Verify requirements.txt has all dependencies
   - Check Python version compatibility

2. **Deployment fails**:
   - Check application logs
   - Verify environment variables
   - Test locally first

3. **App won't start**:
   - Check port configuration
   - Verify all API keys are valid
   - Check memory/resource limits

### Getting Help

1. **Check logs**:
   ```bash
   # Heroku
   heroku logs --tail
   
   # Railway
   # Check logs in Railway dashboard
   
   # GitHub Actions
   # Check Actions tab in repository
   ```

2. **Debug locally**:
   ```bash
   # Test the exact production setup
   docker-compose -f docker-compose.prod.yml up
   ```

## 🎉 Success!

Once deployed, your FloatChat application will be available at:
- **Heroku**: `https://your-app-name.herokuapp.com`
- **Railway**: `https://your-app-name.railway.app`
- **Render**: `https://your-app-name.onrender.com`

### Share your deployment:

```markdown
🌊 **FloatChat is now live!**

🔗 **Live Demo**: https://your-app-name.herokuapp.com
📚 **API Docs**: https://your-app-name.herokuapp.com/docs
📖 **GitHub**: https://github.com/YOUR_USERNAME/floatchat

Try asking: "Show me temperature data in Bay of Bengal"
```

---

**Congratulations! Your FloatChat is now deployed and accessible worldwide!** 🌊🚀

## 📞 Support

- **Issues**: Create GitHub Issues for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the `docs/` folder

Happy deploying! 🎉