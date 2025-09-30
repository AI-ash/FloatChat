# FloatChat Cloud APIs Setup Guide

This guide provides **step-by-step instructions** to set up the **5 essential cloud services** required for FloatChat deployment.

## 🎯 **Required Services Overview**

You need **exactly 5 API keys** to run FloatChat:

1. **Supabase** - Database (PostgreSQL + PostGIS)
2. **Groq** - Fast LLM inference 
3. **Pinecone** - Vector database for RAG
4. **Cohere** - Text embeddings
5. **Redis Cloud** - Caching

**Total setup time**: ~15 minutes  
**Total cost**: $0/month (all free tiers)

---

## 🗃️ **Step 1: Database - Supabase**

**What it provides**: Cloud PostgreSQL database with geospatial extensions

### **Setup Steps**:
1. **Go to** [supabase.com](https://supabase.com)
2. **Click** "Start your project" → Sign up with GitHub/Google
3. **Create new project**:
   - Project name: `floatchat`
   - Database password: Create a strong password (save it!)
   - Region: Choose closest to you
4. **Wait** for project initialization (2-3 minutes)
5. **Get connection string**:
   - Go to Settings → Database
   - Copy the "Connection string" (URI format)
   - Replace `[YOUR-PASSWORD]` with your actual password
6. **Enable PostGIS** (for geospatial data):
   - Go to SQL Editor
   - Run: `CREATE EXTENSION IF NOT EXISTS postgis;`
   - Click "Run"

### **Copy this to your .env file**:
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```

**✅ Free tier**: 500MB database, 2GB bandwidth/month

---

## 🤖 **Step 2: AI/LLM - Groq**

**What it provides**: Ultra-fast LLaMA-3 inference (primary LLM)

### **Setup Steps**:
1. **Go to** [console.groq.com](https://console.groq.com)
2. **Sign up** with Google/GitHub (no phone verification needed)
3. **Create API key**:
   - Click "API Keys" in left sidebar
   - Click "Create API Key"
   - Name: `floatchat`
   - Click "Submit"
4. **Copy the key** (starts with `gsk_`) - save it immediately!

### **Copy this to your .env file**:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**✅ Free tier**: 30 requests/minute, 6000 tokens/minute

---

## 🔍 **Step 3: Vector Database - Pinecone**

**What it provides**: Managed vector database for RAG knowledge base

### **Setup Steps**:
1. **Go to** [pinecone.io](https://pinecone.io)
2. **Sign up** for free account (email + password)
3. **Create index**:
   - Click "Create Index"
   - Index name: `floatchat-knowledge`
   - Dimensions: `1024`
   - Metric: `cosine`
   - Environment: `us-east-1` (free tier)
   - Click "Create Index"
4. **Get API key**:
   - Go to "API Keys" tab
   - Copy the API key
   - Note the Environment (should be `us-east-1`)

### **Copy this to your .env file**:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=floatchat-knowledge
```

**✅ Free tier**: 1 index, 5M vectors

---

## 📝 **Step 4: Embeddings - Cohere**

**What it provides**: High-quality text embeddings for RAG

### **Setup Steps**:
1. **Go to** [cohere.com](https://cohere.com)
2. **Sign up** for free account
3. **Get API key**:
   - Go to dashboard after signup
   - Click "API Keys" 
   - Copy the default API key

### **Copy this to your .env file**:
```env
COHERE_API_KEY=your_cohere_api_key_here
```

**✅ Free tier**: 100 API calls/month

---

## 💾 **Step 5: Caching - Redis Cloud**

**What it provides**: In-memory caching for API responses and data

### **Setup Steps**:
1. **Go to** [redis.com/try-free](https://redis.com/try-free)
2. **Sign up** for free account
3. **Create database**:
   - Click "New database"
   - Name: `floatchat-cache`
   - Cloud: AWS
   - Region: Choose closest to you
   - Click "Activate database"
4. **Get connection URL**:
   - Click on your database name
   - Copy the "Public endpoint" URL
   - Format: `redis://default:password@host:port`

### **Copy this to your .env file**:
```env
REDIS_URL=redis://default:your_password@your-host:port
```

**✅ Free tier**: 30MB storage

---

## 🎉 **Setup Complete!**

You now have all 5 API keys. Your `.env` file should look like this:

```env
# Essential Services (5 APIs)
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
GROQ_API_KEY=gsk_your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=floatchat-knowledge
COHERE_API_KEY=your_cohere_api_key
REDIS_URL=redis://default:password@host:port

# Data Sources (No API keys needed)
ARGO_API_BASE=https://data-argo.ifremer.fr
ERDDAP_BASE=https://www.ifremer.fr/erddap
NOAA_ERDDAP_BASE=https://coastwatch.pfeg.noaa.gov/erddap
COPERNICUS_MARINE_BASE=https://marine.copernicus.eu
```

---

## 🚀 **Next Steps**

### **1. Test Your Setup**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your 5 API keys
nano .env  # or use any text editor

# Test the configuration
python test_setup.py
```

### **2. Start FloatChat**:
```bash
python start.py
```

### **3. Access the Application**:
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 💰 **Cost Breakdown**

### **Free Tier (Development)**:
- **Supabase**: Free (500MB database)
- **Groq**: Free (30 req/min)
- **Pinecone**: Free (5M vectors)
- **Cohere**: Free (100 calls/month)
- **Redis Cloud**: Free (30MB)
- **Total**: **$0/month**

### **Production Scale** (1000+ users):
- **Supabase Pro**: $25/month
- **Groq**: $50/month (higher limits)
- **Pinecone**: $70/month (more vectors)
- **Cohere**: $20/month (more calls)
- **Redis Cloud**: $15/month (1GB)
- **Total**: **~$180/month**

---

## 🆘 **Troubleshooting**

### **Common Issues**:

1. **Database connection fails**:
   - Check if your IP is whitelisted in Supabase
   - Verify the password in your DATABASE_URL

2. **Groq API rate limits**:
   - Free tier: 30 requests/minute
   - Wait or upgrade for higher limits

3. **Pinecone index not found**:
   - Ensure index name is exactly `floatchat-knowledge`
   - Check environment is `us-east-1`

4. **Redis connection timeout**:
   - Verify Redis URL format is correct
   - Check if Redis instance is active

5. **Import errors**:
   - Run `pip install -r requirements.txt`
   - Make sure you're in the correct virtual environment

---

## 📞 **Support**

- **Supabase**: support@supabase.io
- **Groq**: support@groq.com  
- **Pinecone**: support@pinecone.io
- **Cohere**: support@cohere.com
- **Redis**: support@redis.com

---

## 🎉 **You're Ready!**

With these 5 API keys, FloatChat will run completely in the cloud with:
- ✅ **No local installations** (except Python)
- ✅ **No file storage** (everything in memory)
- ✅ **No registration delays** (all instant access)
- ✅ **$0 cost** for development
- ✅ **Global ocean data** access

**Happy ocean data exploring!** 🌊