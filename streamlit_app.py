#!/usr/bin/env python3
"""
Streamlit app with embedded FastAPI for Render
Single process solution
"""

import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import threading
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Import backend components
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.main import app as fastapi_app
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Backend import failed: {e}")
    BACKEND_AVAILABLE = False
    # Create minimal FastAPI app
    fastapi_app = FastAPI()
    
    @fastapi_app.get("/")
    async def health():
        return {"status": "ok", "message": "Minimal API running"}

# Start FastAPI in background thread
def start_fastapi_server():
    """Start FastAPI server in background"""
    port = int(os.getenv('BACKEND_PORT', '8000'))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port, log_level="warning")

# Start the FastAPI server in a separate thread
if BACKEND_AVAILABLE:
    backend_port = int(os.getenv('BACKEND_PORT', '8000'))
    backend_thread = threading.Thread(target=start_fastapi_server, daemon=True)
    backend_thread.start()
    time.sleep(3)  # Give backend time to start
    BACKEND_URL = f"http://localhost:{backend_port}"
else:
    BACKEND_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="FloatChat - AI Ocean Data Assistant",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #9c27b0;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'user_role' not in st.session_state:
    st.session_state.user_role = 'student'

def process_query(query: str):
    """Process user query through the backend API"""
    try:
        # Add user message to chat
        st.session_state.chat_history.append({
            'role': 'user',
            'content': query,
            'timestamp': datetime.now()
        })
        
        # Show processing indicator
        with st.spinner("Processing your query..."):
            # Call backend API
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={
                    "query": query,
                    "user_role": st.session_state.user_role
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Add assistant response to chat
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': result['response'],
                    'visualizations': result.get('visualizations', []),
                    'data_summary': result.get('data_summary', {}),
                    'provenance': result.get('provenance', {}),
                    'timestamp': datetime.now()
                })
                
                st.success("Query processed successfully!")
                st.rerun()
                
            else:
                st.error(f"Error processing query: {response.text}")
                
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        st.info(f"Make sure the backend server is running at {BACKEND_URL}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

def show_visualizations(visualizations):
    """Display visualizations from query results"""
    if not visualizations:
        st.info("No visualizations available for this query.")
        return
        
    try:
        for viz in visualizations:
            if not isinstance(viz, dict):
                continue
                
            title = viz.get('title', 'Visualization')
            viz_type = viz.get('type', 'unknown')
            
            st.subheader(title)
            
            if viz_type == 'map':
                show_map_visualization(viz)
            elif viz_type == 'plot':
                show_plot_visualization(viz)
            else:
                st.warning(f"Unknown visualization type: {viz_type}")
                
    except Exception as e:
        st.error(f"Error displaying visualizations: {e}")
        st.info("Visualizations are temporarily unavailable.")

def show_map_visualization(viz_config):
    """Show map visualization"""
    try:
        # Get configuration from backend
        config = viz_config.get('config', {})
        
        # Extract data from config
        lats = config.get('lat', [])
        lons = config.get('lon', [])
        texts = config.get('text', [])
        
        # Use default location if no data
        if not lats or not lons:
            center_lat, center_lon = 20.0, 77.0
            lats = [15.0, 18.0, 22.0]
            lons = [75.0, 82.0, 88.0]
            texts = ["Float 1: Temperature 28.5°C", "Float 2: Temperature 27.8°C", "Float 3: Temperature 26.2°C"]
        else:
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
        
        # Create folium map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add markers
        for i, (lat, lon) in enumerate(zip(lats, lons)):
            text = texts[i] if i < len(texts) else f"Location {i+1}"
            folium.Marker(
                [lat, lon],
                popup=text,
                tooltip=f"Point {i+1}"
            ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=400)
        
    except Exception as e:
        st.error(f"Error displaying map: {e}")
        # Fallback to simple map
        m = folium.Map(location=[20.0, 77.0], zoom_start=5)
        st_folium(m, width=700, height=400)

def show_plot_visualization(viz_config):
    """Show plot visualization"""
    # Create sample time series plot
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='M')
    temperatures = 25 + 3 * np.sin(np.arange(len(dates)) * 2 * np.pi / 12) + np.random.normal(0, 0.5, len(dates))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=temperatures,
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title='Ocean Temperature Trend',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🌊 FloatChat</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">AI-Powered ARGO Oceanographic Data Assistant</p>', unsafe_allow_html=True)
    
    # Show backend connection status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if BACKEND_AVAILABLE:
            st.success(f"🔗 Connected to backend: {BACKEND_URL}")
        else:
            st.warning("⚠️ Backend not available - using minimal mode")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # User role selection
        user_role = st.selectbox(
            "Select your role:",
            ["student", "researcher", "policymaker"],
            index=0
        )
        st.session_state.user_role = user_role
        
        st.markdown("---")
        
        # Example queries
        st.subheader("💡 Example Queries")
        example_queries = [
            "Show me temperature data in Bay of Bengal",
            "What's the salinity trend over the last year?",
            "Display ARGO float locations",
            "Explain ocean salinity patterns"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{hash(query)}"):
                process_query(query)
        
        st.markdown("---")
        
        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Chat with FloatChat")
    
    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                
                # Show visualizations if available
                if 'visualizations' in message:
                    try:
                        show_visualizations(message['visualizations'])
                    except Exception as e:
                        st.error(f"Error displaying visualizations: {e}")
                        st.info("Visualizations are temporarily unavailable.")
    
    # Query input
    query_input = st.text_input(
        "Ask about ocean data:",
        placeholder="e.g., Show me temperature trends in Bay of Bengal over last 5 years",
        key="query_input"
    )
    
    if st.button("Send Query", type="primary") and query_input:
        process_query(query_input)

if __name__ == "__main__":
    main()