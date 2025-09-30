<<<<<<< HEAD
# FloatChat Cloud Setup Guide

This guide will help you set up and deploy the FloatChat AI-powered ARGO data system using cloud services only.

## Prerequisites

### System Requirements
- Python 3.9 or higher
- Internet connection for cloud APIs
- Cloud service accounts (see API setup guide)
- No local database or LLM installation required!

### Required Accounts

**Essential Cloud Services** (all have free tiers):
1. **Supabase** - Cloud PostgreSQL database
2. **Groq** - Fast LLaMA inference API  
3. **Pinecone** - Vector database for RAG
4. **Cohere** - Text embeddings API
5. **Redis Cloud** - Caching service
6. **AWS S3** - File storage

**Optional Services**:
- OpenAI API (backup LLM)
- Bhashini API (Indian languages)
- Sentry (error monitoring)

### Setup Process

1. **Get API Keys** - Follow the [Cloud APIs Setup Guide](CLOUD_APIS_SETUP.md)
2. **Configure Environment** - Set up all API keys
3. **Deploy Application** - Use cloud deployment platforms

## Installation Methods

### Method 1: Cloud Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd floatchat
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Cloud APIs**
   ```bash
   # Follow the detailed guide
   # See: docs/CLOUD_APIS_SETUP.md
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your cloud API keys (see CLOUD_APIS_SETUP.md)
   ```

6. **Initialize Cloud Database**
   ```bash
   python -c "from backend.database import create_tables; create_tables()"
   ```

7. **Run the Application**
   ```bash
   # Start all services
   python run.py

   # Or start individual services
   python run.py --mode backend    # API only
   python run.py --mode frontend   # UI only
   python run.py --mode ingestion  # Data ingestion only
   ```

### Method 2: Docker Cloud Deployment

1. **Clone and Configure**
   ```bash
   git clone <repository-url>
   cd floatchat
   cp .env.example .env
   # Edit .env with all cloud API keys (see CLOUD_APIS_SETUP.md)
   ```

2. **Start with Docker Compose**
   ```bash
   # Start all services (now cloud-based)
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop services
   docker-compose down
   ```

### Method 3: Cloud Platform Deployment

#### Option A: Vercel + Railway
```bash
# Deploy frontend to Vercel
npm i -g vercel
vercel --prod

# Deploy backend to Railway
# Connect GitHub repo to Railway dashboard
```

#### Option B: Heroku
```bash
# Install Heroku CLI
# Create Heroku apps
heroku create floatchat-backend
heroku create floatchat-frontend

# Deploy
git push heroku main
```

#### Option C: DigitalOcean App Platform
```bash
# Use DigitalOcean dashboard
# Connect GitHub repository
# Configure environment variables
```

## Configuration

### Cloud Database Configuration

Edit your `.env` file:
```env
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
```

### AI Services Configuration

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENAI_API_KEY=sk-your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### Cloud Storage Configuration

```env
REDIS_URL=redis://default:password@your-redis-url:port
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_secret_key
CLOUD_STORAGE_BUCKET=floatchat-data
```

### Data Sources (APIs)

```env
ARGO_API_BASE=https://data-argo.ifremer.fr
INCOIS_API_BASE=https://incois.gov.in/portal/datainfo
ERDDAP_BASE=https://www.ifremer.fr/erddap
```

## Verification

### Check Services

1. **Backend API**: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/

2. **Frontend Application**: http://localhost:8501

3. **Cloud Database Connection**
   ```bash
   python -c "from backend.database import engine; print('Cloud DB OK' if engine.connect() else 'DB Error')"
   ```

4. **AI Services**
   ```bash
   # Test Groq API
   python -c "
   from groq import Groq
   client = Groq(api_key='your_key')
   print('Groq API: OK')
   "
   
   # Test Pinecone
   python -c "
   import pinecone
   pinecone.init(api_key='your_key', environment='us-west1-gcp-free')
   print('Pinecone: OK')
   "
   ```

5. **Cloud Storage**
   ```bash
   # Test Redis
   python -c "
   import redis
   r = redis.from_url('your_redis_url')
   r.ping()
   print('Redis: OK')
   "
   ```

### Test Basic Functionality

1. Open the frontend at http://localhost:8501
2. Try a simple query: "Show me recent ARGO float data"
3. Check if visualizations appear
4. Verify data export functionality

## Data Ingestion

### Initial Data Load

```bash
# Run manual ingestion
python -c "
import asyncio
from data.ingestion.argo_ingester import run_ingestion
asyncio.run(run_ingestion())
"
```

### Automated Ingestion

The system automatically ingests new ARGO data every hour when running in full mode.

## Troubleshooting

### Common Issues

1. **Cloud Database Connection Error**
   - Verify Supabase project is active
   - Check database URL format
   - Ensure SSL mode is enabled
   - Whitelist your IP in Supabase dashboard

2. **AI API Rate Limits**
   - Check API key validity
   - Monitor usage in provider dashboards
   - Implement exponential backoff
   - Use multiple providers for redundancy

3. **Frontend Not Loading**
   - Verify backend is running and accessible
   - Check CORS settings for cloud deployment
   - Ensure environment variables are set
   - Check browser console for errors

4. **Vector Database Issues**
   - Verify Pinecone index exists
   - Check index dimensions match embeddings
   - Ensure API key has correct permissions

5. **Storage/Cache Issues**
   - Verify Redis Cloud instance is active
   - Check S3 bucket permissions
   - Ensure AWS credentials are valid

### Performance Optimization

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_argo_profiles_location ON argo_profiles USING GIST(location);
   CREATE INDEX idx_argo_profiles_date ON argo_profiles(profile_date);
   CREATE INDEX idx_argo_profiles_float_id ON argo_profiles(float_id);
   ```

2. **LLM Optimization**
   - Use GPU acceleration if available
   - Consider smaller models for faster response
   - Implement response caching

3. **Data Caching**
   - Enable Redis for query caching
   - Use DuckDB for analytical queries
   - Implement data partitioning

## Development

### Adding New Features

1. **Backend API Endpoints**
   - Add routes in `backend/main.py`
   - Create models in `backend/models.py`
   - Implement services in `backend/services/`

2. **Frontend Components**
   - Add pages in `frontend/`
   - Create visualizations using Plotly/Folium
   - Implement user interface components

3. **Data Processing**
   - Add ingestion scripts in `data/ingestion/`
   - Create analysis pipelines in `ai/`
   - Implement quality control checks

### Testing

```bash
# Run tests
pytest tests/

# Run specific test categories
pytest tests/test_api.py
pytest tests/test_ingestion.py
pytest tests/test_llm.py
```

## Production Deployment

### Security Considerations

1. **Environment Variables**
   - Use secure passwords
   - Enable SSL/TLS
   - Configure firewall rules

2. **Database Security**
   - Restrict database access
   - Use connection pooling
   - Enable query logging

3. **API Security**
   - Implement rate limiting
   - Add authentication if needed
   - Use HTTPS in production

### Monitoring

1. **Application Monitoring**
   - Set up logging aggregation
   - Monitor API response times
   - Track data ingestion status

2. **System Monitoring**
   - Monitor database performance
   - Track memory and CPU usage
   - Set up alerts for failures

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review application logs in `logs/` directory
3. Check GitHub issues for known problems
4. Contact the development team

## Next Steps

After successful setup:
1. Explore the user interface and try different queries
2. Review the API documentation
3. Set up automated data ingestion
4. Configure monitoring and alerts
=======
# FloatChat Cloud Setup Guide

This guide will help you set up and deploy the FloatChat AI-powered ARGO data system using cloud services only.

## Prerequisites

### System Requirements
- Python 3.9 or higher
- Internet connection for cloud APIs
- Cloud service accounts (see API setup guide)
- No local database or LLM installation required!

### Required Accounts

**Essential Cloud Services** (all have free tiers):
1. **Supabase** - Cloud PostgreSQL database
2. **Groq** - Fast LLaMA inference API  
3. **Pinecone** - Vector database for RAG
4. **Cohere** - Text embeddings API
5. **Redis Cloud** - Caching service
6. **AWS S3** - File storage

**Optional Services**:
- OpenAI API (backup LLM)
- Bhashini API (Indian languages)
- Sentry (error monitoring)

### Setup Process

1. **Get API Keys** - Follow the [Cloud APIs Setup Guide](CLOUD_APIS_SETUP.md)
2. **Configure Environment** - Set up all API keys
3. **Deploy Application** - Use cloud deployment platforms

## Installation Methods

### Method 1: Cloud Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd floatchat
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Cloud APIs**
   ```bash
   # Follow the detailed guide
   # See: docs/CLOUD_APIS_SETUP.md
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your cloud API keys (see CLOUD_APIS_SETUP.md)
   ```

6. **Initialize Cloud Database**
   ```bash
   python -c "from backend.database import create_tables; create_tables()"
   ```

7. **Run the Application**
   ```bash
   # Start all services
   python run.py

   # Or start individual services
   python run.py --mode backend    # API only
   python run.py --mode frontend   # UI only
   python run.py --mode ingestion  # Data ingestion only
   ```

### Method 2: Docker Cloud Deployment

1. **Clone and Configure**
   ```bash
   git clone <repository-url>
   cd floatchat
   cp .env.example .env
   # Edit .env with all cloud API keys (see CLOUD_APIS_SETUP.md)
   ```

2. **Start with Docker Compose**
   ```bash
   # Start all services (now cloud-based)
   docker-compose up -d

   # View logs
   docker-compose logs -f

   # Stop services
   docker-compose down
   ```

### Method 3: Cloud Platform Deployment

#### Option A: Vercel + Railway
```bash
# Deploy frontend to Vercel
npm i -g vercel
vercel --prod

# Deploy backend to Railway
# Connect GitHub repo to Railway dashboard
```

#### Option B: Heroku
```bash
# Install Heroku CLI
# Create Heroku apps
heroku create floatchat-backend
heroku create floatchat-frontend

# Deploy
git push heroku main
```

#### Option C: DigitalOcean App Platform
```bash
# Use DigitalOcean dashboard
# Connect GitHub repository
# Configure environment variables
```

## Configuration

### Cloud Database Configuration

Edit your `.env` file:
```env
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
```

### AI Services Configuration

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
OPENAI_API_KEY=sk-your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

### Cloud Storage Configuration

```env
REDIS_URL=redis://default:password@your-redis-url:port
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_secret_key
CLOUD_STORAGE_BUCKET=floatchat-data
```

### Data Sources (APIs)

```env
ARGO_API_BASE=https://data-argo.ifremer.fr
INCOIS_API_BASE=https://incois.gov.in/portal/datainfo
ERDDAP_BASE=https://www.ifremer.fr/erddap
```

## Verification

### Check Services

1. **Backend API**: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/

2. **Frontend Application**: http://localhost:8501

3. **Cloud Database Connection**
   ```bash
   python -c "from backend.database import engine; print('Cloud DB OK' if engine.connect() else 'DB Error')"
   ```

4. **AI Services**
   ```bash
   # Test Groq API
   python -c "
   from groq import Groq
   client = Groq(api_key='your_key')
   print('Groq API: OK')
   "
   
   # Test Pinecone
   python -c "
   import pinecone
   pinecone.init(api_key='your_key', environment='us-west1-gcp-free')
   print('Pinecone: OK')
   "
   ```

5. **Cloud Storage**
   ```bash
   # Test Redis
   python -c "
   import redis
   r = redis.from_url('your_redis_url')
   r.ping()
   print('Redis: OK')
   "
   ```

### Test Basic Functionality

1. Open the frontend at http://localhost:8501
2. Try a simple query: "Show me recent ARGO float data"
3. Check if visualizations appear
4. Verify data export functionality

## Data Ingestion

### Initial Data Load

```bash
# Run manual ingestion
python -c "
import asyncio
from data.ingestion.argo_ingester import run_ingestion
asyncio.run(run_ingestion())
"
```

### Automated Ingestion

The system automatically ingests new ARGO data every hour when running in full mode.

## Troubleshooting

### Common Issues

1. **Cloud Database Connection Error**
   - Verify Supabase project is active
   - Check database URL format
   - Ensure SSL mode is enabled
   - Whitelist your IP in Supabase dashboard

2. **AI API Rate Limits**
   - Check API key validity
   - Monitor usage in provider dashboards
   - Implement exponential backoff
   - Use multiple providers for redundancy

3. **Frontend Not Loading**
   - Verify backend is running and accessible
   - Check CORS settings for cloud deployment
   - Ensure environment variables are set
   - Check browser console for errors

4. **Vector Database Issues**
   - Verify Pinecone index exists
   - Check index dimensions match embeddings
   - Ensure API key has correct permissions

5. **Storage/Cache Issues**
   - Verify Redis Cloud instance is active
   - Check S3 bucket permissions
   - Ensure AWS credentials are valid

### Performance Optimization

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_argo_profiles_location ON argo_profiles USING GIST(location);
   CREATE INDEX idx_argo_profiles_date ON argo_profiles(profile_date);
   CREATE INDEX idx_argo_profiles_float_id ON argo_profiles(float_id);
   ```

2. **LLM Optimization**
   - Use GPU acceleration if available
   - Consider smaller models for faster response
   - Implement response caching

3. **Data Caching**
   - Enable Redis for query caching
   - Use DuckDB for analytical queries
   - Implement data partitioning

## Development

### Adding New Features

1. **Backend API Endpoints**
   - Add routes in `backend/main.py`
   - Create models in `backend/models.py`
   - Implement services in `backend/services/`

2. **Frontend Components**
   - Add pages in `frontend/`
   - Create visualizations using Plotly/Folium
   - Implement user interface components

3. **Data Processing**
   - Add ingestion scripts in `data/ingestion/`
   - Create analysis pipelines in `ai/`
   - Implement quality control checks

### Testing

```bash
# Run tests
pytest tests/

# Run specific test categories
pytest tests/test_api.py
pytest tests/test_ingestion.py
pytest tests/test_llm.py
```

## Production Deployment

### Security Considerations

1. **Environment Variables**
   - Use secure passwords
   - Enable SSL/TLS
   - Configure firewall rules

2. **Database Security**
   - Restrict database access
   - Use connection pooling
   - Enable query logging

3. **API Security**
   - Implement rate limiting
   - Add authentication if needed
   - Use HTTPS in production

### Monitoring

1. **Application Monitoring**
   - Set up logging aggregation
   - Monitor API response times
   - Track data ingestion status

2. **System Monitoring**
   - Monitor database performance
   - Track memory and CPU usage
   - Set up alerts for failures

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review application logs in `logs/` directory
3. Check GitHub issues for known problems
4. Contact the development team

## Next Steps

After successful setup:
1. Explore the user interface and try different queries
2. Review the API documentation
3. Set up automated data ingestion
4. Configure monitoring and alerts
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
5. Customize the system for your specific use case