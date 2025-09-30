#!/usr/bin/env python3
"""
Simple FastAPI app for Render deployment
Minimal dependencies, maximum reliability
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

# Create FastAPI app
app = FastAPI(
    title="FloatChat",
    description="AI-Powered ARGO Data System",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str
    user_role: str = "student"

# Simple HTML interface
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>FloatChat - AI Ocean Data Assistant</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container { 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { 
            text-align: center; 
            color: #fff;
            margin-bottom: 30px;
        }
        .status {
            background: rgba(76, 175, 80, 0.2);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 FloatChat</h1>
        <p style="text-align: center; margin-bottom: 30px;">
            AI-Powered Oceanographic Data Assistant
        </p>
        
        <div class="status">
            <h3>✅ System Status</h3>
            <p>🚀 Backend API: Running</p>
            <p>🔗 Deployment: Render.com</p>
            <p>📚 API Documentation: <a href="/docs" style="color: #ffeb3b;">/docs</a></p>
        </div>
        
        <div class="feature">
            <h3>🌊 Features</h3>
            <ul>
                <li>🗣️ Natural Language Queries</li>
                <li>📊 Real-time Oceanographic Data</li>
                <li>🤖 AI-Powered Analysis</li>
                <li>📈 Interactive Visualizations</li>
                <li>🌐 RESTful API</li>
            </ul>
        </div>
        
        <div class="feature">
            <h3>🔗 API Endpoints</h3>
            <ul>
                <li><strong>GET /</strong> - This web interface</li>
                <li><strong>GET /docs</strong> - API documentation</li>
                <li><strong>GET /health</strong> - Health check</li>
                <li><strong>POST /api/query</strong> - Process queries</li>
            </ul>
        </div>
        
        <div class="feature">
            <h3>💡 Example Usage</h3>
            <p>Send a POST request to <code>/api/query</code>:</p>
            <pre style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px;">
{
  "query": "Show me temperature data in Bay of Bengal",
  "user_role": "student"
}
            </pre>
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_web_interface():
    """Serve the web interface"""
    return HTML_INTERFACE

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FloatChat",
        "version": "1.0.0",
        "deployment": "render"
    }

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process oceanographic queries"""
    
    # Simple mock response for now
    response = {
        "query": request.query,
        "response": f"I understand you're asking about: '{request.query}'. This is a mock response from the simplified FloatChat API. The full AI-powered system with real oceanographic data processing is being deployed.",
        "data_summary": {
            "record_count": 24,
            "variables": ["temperature", "salinity"],
            "data_sources": ["Mock Data Service"],
            "spatial_coverage": {
                "min_lat": 10.0,
                "max_lat": 25.0,
                "min_lon": 70.0,
                "max_lon": 90.0
            }
        },
        "processing_time": 0.1,
        "status": "success"
    }
    
    return response

@app.get("/api/variables")
async def get_variables():
    """Get available oceanographic variables"""
    return {
        "variables": [
            "temperature",
            "salinity", 
            "pressure",
            "oxygen",
            "chlorophyll"
        ]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    print(f"🌊 Starting FloatChat Simple on port {port}")
    print(f"🔗 Web Interface: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "app_simple:app",
        host="0.0.0.0",
        port=port,
        workers=1
    )