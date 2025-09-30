#!/usr/bin/env python3
"""
Combined FastAPI + Streamlit app for Render deployment
Serves both API and web interface on the same port
"""

import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import subprocess
import threading
import time

# Import the existing FastAPI app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.main import app as backend_app

# Create a simple HTML interface that connects to the API
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
        .query-box { 
            width: 100%; 
            padding: 15px; 
            font-size: 16px; 
            border: none;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .send-btn { 
            background: #4CAF50; 
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        .send-btn:hover { background: #45a049; }
        .response { 
            background: rgba(255,255,255,0.2); 
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 20px;
            min-height: 100px;
        }
        .loading { color: #ffeb3b; }
        .error { color: #f44336; }
        .success { color: #4CAF50; }
        .examples {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }
        .example {
            cursor: pointer;
            padding: 8px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            transition: background 0.3s;
        }
        .example:hover {
            background: rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 FloatChat</h1>
        <p style="text-align: center; margin-bottom: 30px;">
            AI-Powered Oceanographic Data Assistant
        </p>
        
        <input type="text" id="queryInput" class="query-box" 
               placeholder="Ask about ocean data... e.g., 'Show me temperature data in Bay of Bengal'">
        
        <button onclick="sendQuery()" class="send-btn">Send Query</button>
        
        <div id="response" class="response">
            <p>👋 Welcome to FloatChat! Ask me anything about oceanographic data.</p>
            <p>🔗 <strong>API Documentation:</strong> <a href="/docs" style="color: #ffeb3b;">/docs</a></p>
            <p>🔍 <strong>Health Check:</strong> <a href="/" style="color: #ffeb3b;">API Status</a></p>
        </div>
        
        <div class="examples">
            <h3>💡 Example Queries:</h3>
            <div class="example" onclick="setQuery(this.textContent)">
                Show me temperature data in Bay of Bengal
            </div>
            <div class="example" onclick="setQuery(this.textContent)">
                What's the salinity trend over the last year?
            </div>
            <div class="example" onclick="setQuery(this.textContent)">
                Display ARGO float locations
            </div>
            <div class="example" onclick="setQuery(this.textContent)">
                Explain ocean salinity patterns
            </div>
        </div>
    </div>

    <script>
        function setQuery(text) {
            document.getElementById('queryInput').value = text;
        }
        
        async function sendQuery() {
            const query = document.getElementById('queryInput').value;
            const responseDiv = document.getElementById('response');
            
            if (!query.trim()) {
                responseDiv.innerHTML = '<p class="error">Please enter a query!</p>';
                return;
            }
            
            responseDiv.innerHTML = '<p class="loading">🔄 Processing your query...</p>';
            
            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        query: query,
                        user_role: 'student'
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    responseDiv.innerHTML = `
                        <div class="success">
                            <h3>🤖 Assistant Response:</h3>
                            <p>${data.response}</p>
                            <hr>
                            <p><strong>📊 Data Records:</strong> ${data.data_summary.record_count}</p>
                            <p><strong>🗂️ Data Sources:</strong> ${data.data_summary.data_sources.join(', ')}</p>
                            <p><strong>📈 Variables:</strong> ${data.data_summary.variables.join(', ')}</p>
                            <p><strong>⏱️ Processing Time:</strong> ${data.processing_time.toFixed(2)}s</p>
                        </div>
                    `;
                } else {
                    const errorText = await response.text();
                    responseDiv.innerHTML = `<p class="error">❌ Error: ${errorText}</p>`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<p class="error">❌ Connection Error: ${error.message}</p>`;
            }
        }
        
        // Allow Enter key to send query
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendQuery();
            }
        });
    </script>
</body>
</html>
"""

# Add the HTML interface to the FastAPI app
@backend_app.get("/", response_class=HTMLResponse)
async def get_web_interface():
    """Serve the web interface"""
    return HTML_INTERFACE

@backend_app.get("/web", response_class=HTMLResponse)
async def get_web_interface_alt():
    """Alternative route for web interface"""
    return HTML_INTERFACE

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    print(f"🌊 Starting FloatChat on port {port}")
    print(f"🔗 Web Interface: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    
    uvicorn.run(
        "app_render:backend_app",
        host="0.0.0.0",
        port=port,
        workers=1
    )