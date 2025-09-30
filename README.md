# FloatChat - AI-Powered ARGO Data System

A cloud-native intelligent oceanographic data platform that enables natural language querying, analysis, and visualization of ARGO float data through conversational AI.

## 🌊 Overview

FloatChat is designed for SIH 2025 PS to democratize access to oceanographic data through:
- Natural language Q/A with cloud-based LLMs (Groq, OpenAI)
- Automated data ingestion and quality control via APIs
- Real-time and historical ARGO data analysis
- Interactive maps and visualizations
- Multi-user role-based interfaces
- **100% Cloud-based - No local installations required!**

## 🚀 Features

- **Conversational AI**: Query ocean data using natural language via Groq/OpenAI APIs
- **Cloud Data Pipeline**: NetCDF, CSV, API ingestion with QC flags stored in cloud
- **Smart Visualization**: Auto-generated maps, plots, and 3D trajectories
- **RAG-powered Insights**: Vector search with Pinecone for oceanographic knowledge
- **Multi-User Support**: Student, researcher, and policymaker dashboards
- **Data Provenance**: Full traceability of data sources and quality flags

## 🛠️ Cloud-First Tech Stack

- **Database**: Supabase (PostgreSQL + PostGIS)
- **AI/LLM**: Groq (LLaMA-3), OpenAI (GPT-3.5/4), Cohere (Embeddings)
- **Vector DB**: Pinecone for RAG knowledge base
- **Storage**: In-memory processing, Redis Cloud for caching
- **Frontend**: Streamlit with cloud deployment
- **Backend**: FastAPI with cloud APIs integration
- **Visualization**: Leaflet.js, Plotly, CesiumJS
- **Data Sources**: ARGO, ERDDAP, NOAA, Copernicus Marine APIs

## 📁 Project Structure

```
floatchat/
├── backend/           # FastAPI backend services
├── frontend/          # Streamlit frontend
├── data/             # Data ingestion and processing
├── ai/               # LLM and ML components
├── visualization/    # Maps and plotting utilities
├── config/           # Configuration files
└── docs/             # Documentation
```

## 🏃‍♂️ Quick Start

1. **Get Cloud API Keys** (all have free tiers):
   - [Supabase](https://supabase.com) - Database
   - [Groq](https://console.groq.com) - Fast LLM inference  
   - [Pinecone](https://pinecone.io) - Vector database
   - [Cohere](https://cohere.com) - Embeddings
   - [Redis Cloud](https://redis.com) - Caching

2. **Setup Environment**:
   ```bash
   git clone <repository-url>
   cd floatchat
   cp .env.example .env
   # Fill in your API keys in .env file
   ```

3. **Test Setup**:
   ```bash
   python test_setup.py
   ```

4. **Start Application**:
   ```bash
   python start.py
   ```

5. **Access Application**:
   - Frontend: http://localhost:8501
   - API: http://localhost:8000/docs

📖 **Detailed Setup**: See [Cloud APIs Setup Guide](docs/CLOUD_APIS_SETUP.md)

## 🎯 Use Cases

- "Show me salinity trends in Bay of Bengal over last 10 years"
- "What's the temperature profile near my location at 500m depth?"
- "Detect El Niño events from ARGO data"
- "Export oxygen data for research publication"

## 💰 Cost-Effective Cloud Deployment

**Free Tier Usage** (Perfect for development/testing):
- All services offer generous free tiers
- Total cost: **$0/month** for small-scale usage
- Scales automatically with usage

**Production Usage** (1000+ users):
- Estimated cost: **~$280/month**
- Includes high-availability, auto-scaling
- No infrastructure management required

## 🌐 Deployment Options

### Option 1: Render.com (Recommended for Production)
```bash
# Quick deployment to Render
./deploy-render.sh     # Linux/Mac
deploy-render.bat      # Windows

# Or follow the detailed guide
# See RENDER_DEPLOYMENT.md for complete instructions
```

**Benefits:**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Docker support
- ✅ Easy environment variable management
- ✅ Built-in monitoring

### Option 2: Docker Deployment (Local/Other Platforms)
```bash
# Clone and setup
git clone https://github.com/yourusername/floatchat.git
cd floatchat
cp .env.example .env
# Edit .env with your API keys

# Deploy with Docker
./deploy.sh        # Linux/Mac
deploy.bat         # Windows
```

### Option 3: Local Development
```bash
pip install -r requirements.txt
python run_floatchat.py
```

### Option 4: Other Cloud Platforms
- **Heroku**: `git push heroku main`
- **DigitalOcean**: App Platform integration
- **AWS/GCP**: ECS/Cloud Run deployment
- **Railway**: One-click deploy from GitHub

## 🧪 Testing & Validation

```bash
# Test complete system
python test_complete_system.py

# Test individual components
python test_real_data.py
python test_visualization_fix.py
```

## 📊 System Status

- ✅ **Backend API**: Fast data processing with realistic oceanographic models
- ✅ **Frontend UI**: Interactive Streamlit interface with map visualizations
- ✅ **AI Integration**: Groq LLM for natural language processing
- ✅ **Data Sources**: Marine Weather API, NOAA Tides, Enhanced mock data
- ✅ **Visualizations**: Fixed JSON serialization, working map displays
- ✅ **Docker Ready**: Complete containerization with health checks