#!/bin/bash
# FloatChat Deployment Script

set -e

echo "🌊 FloatChat Deployment Script"
echo "=============================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "💡 Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Build and start services
echo "🔨 Building FloatChat..."
docker-compose build

echo "🚀 Starting FloatChat services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs floatchat
    exit 1
fi

if curl -f http://localhost:8501/ > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️ Frontend may still be starting..."
fi

echo ""
echo "🎉 FloatChat deployed successfully!"
echo "=================================="
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🌊 Frontend: http://localhost:8501"
echo "=================================="
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"