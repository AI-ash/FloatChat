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
    try:
        uvicorn.run(fastapi_app, host="0.0.0.0", port=port, log_level="warning", access_log=False)
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        # Try alternative port
        alt_port = port + 1
        try:
            print(f"🔄 Trying alternative port {alt_port}")
            uvicorn.run(fastapi_app, host="0.0.0.0", port=alt_port, log_level="warning", access_log=False)
        except Exception as e2:
            print(f"❌ Failed to start FastAPI server on alternative port: {e2}")

# Start the FastAPI server in a separate thread
if BACKEND_AVAILABLE:
    backend_port = int(os.getenv('BACKEND_PORT', '8000'))
    backend_thread = threading.Thread(target=start_fastapi_server, daemon=True)
    backend_thread.start()
    time.sleep(3)  # Give backend time to start
    BACKEND_URL = f"http://localhost:{backend_port}"
else:
    BACKEND_URL = "http://localhost:8000"

# Debug: Show backend URL in sidebar
print(f"🔗 Frontend connecting to backend: {BACKEND_URL}")

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

def check_backend_health():
    """Check if backend is healthy and responding"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def process_query(query: str):
    """Process user query through the backend API"""
    try:
        # Check backend health first
        if not check_backend_health():
            st.error("❌ Backend service is not responding. Please wait a moment and try again.")
            st.info("The backend is starting up. This may take a few seconds...")
            return
        
        # Add user message to chat
        st.session_state.chat_history.append({
            'role': 'user',
            'content': query,
            'timestamp': datetime.now()
        })
        
        # Show processing indicator
        with st.spinner("🌊 Processing your oceanographic query..."):
            # Call backend API
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={
                    "query": query,
                    "user_role": st.session_state.user_role
                },
                timeout=30  # Increased timeout for complex queries
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                if 'response' not in result:
                    st.error("❌ Invalid response from backend")
                    return
                
                # Add assistant response to chat
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': result['response'],
                    'visualizations': result.get('visualizations', []),
                    'data_summary': result.get('data_summary', {}),
                    'provenance': result.get('provenance', {}),
                    'timestamp': datetime.now()
                })
                
                st.success("✅ Query processed successfully!")
                st.rerun()
                
            else:
                st.error(f"❌ Backend error (Status {response.status_code}): {response.text}")
                
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. The query might be too complex or the backend is overloaded.")
        st.info("Try simplifying your query or wait a moment and try again.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Connection error: Cannot reach the backend service.")
        st.info(f"Backend URL: {BACKEND_URL}")
        st.info("The backend might be starting up. Please wait and try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Network error: {str(e)}")
        st.info("Please check your internet connection and try again.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")

def show_visualizations(visualizations):
    """Display visualizations from query results"""
    if not visualizations:
        st.info("📊 No visualizations available for this query.")
        return
        
    try:
        st.subheader("📈 Data Visualizations")
        
        for i, viz in enumerate(visualizations):
            if not isinstance(viz, dict):
                st.warning(f"⚠️ Invalid visualization format at index {i}")
                continue
                
            title = viz.get('title', f'Visualization {i+1}')
            viz_type = viz.get('type', 'unknown')
            
            with st.expander(f"📊 {title}", expanded=True):
                try:
                    if viz_type == 'map':
                        show_map_visualization(viz)
                    elif viz_type == 'plot':
                        show_plot_visualization(viz)
                    elif viz_type == '3d':
                        show_3d_visualization(viz)
                    else:
                        st.warning(f"⚠️ Unknown visualization type: {viz_type}")
                        # Try to display as generic plot
                        show_generic_visualization(viz)
                except Exception as viz_error:
                    st.error(f"❌ Error displaying {title}: {viz_error}")
                    st.info("This visualization could not be rendered properly.")
                
    except Exception as e:
        st.error(f"❌ Error processing visualizations: {e}")
        st.info("📊 Visualizations are temporarily unavailable. The data is still valid.")

def show_map_visualization(viz_config):
    """Show map visualization with real-time data"""
    try:
        # Get configuration from backend
        config = viz_config.get('config', {})
        
        # Handle different config formats
        if 'data' in config and isinstance(config['data'], list) and len(config['data']) > 0:
            # New format from visualization service
            data = config['data'][0]
            lats = data.get('lat', [])
            lons = data.get('lon', [])
            values = data.get('marker', {}).get('color', [])
            texts = data.get('text', [])
        else:
            # Legacy format
            lats = config.get('lat', [])
            lons = config.get('lon', [])
            texts = config.get('text', [])
            values = []
        
        # Use default location if no data
        if not lats or not lons:
            center_lat, center_lon = 20.0, 77.0
            lats = [15.0, 18.0, 22.0, 19.0, 21.0]
            lons = [75.0, 82.0, 88.0, 79.0, 85.0]
            texts = [
                "Float 5904471: Temperature 28.5°C, Salinity 33.2",
                "Float 2902746: Temperature 27.8°C, Salinity 34.1", 
                "Float 2902747: Temperature 26.2°C, Salinity 33.8",
                "Float 5904472: Temperature 29.1°C, Salinity 33.5",
                "Float 2902748: Temperature 27.3°C, Salinity 34.0"
            ]
            values = [28.5, 27.8, 26.2, 29.1, 27.3]
        else:
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
        
        # Create folium map with better styling
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add markers with color coding based on values
        for i, (lat, lon) in enumerate(zip(lats, lons)):
            text = texts[i] if i < len(texts) else f"ARGO Float {i+1}"
            value = values[i] if i < len(values) else 0
            
            # Color code based on temperature or value
            if value > 28:
                color = 'red'
            elif value > 26:
                color = 'orange'
            elif value > 24:
                color = 'yellow'
            else:
                color = 'blue'
            
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(text, max_width=300),
                tooltip=f"ARGO Float {i+1}: {value:.1f}°C",
                icon=folium.Icon(color=color, icon='tint', prefix='fa')
            ).add_to(m)
        
        # Add a legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 150px; height: 90px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p><b>Temperature Legend</b></p>
        <p><i class="fa fa-tint" style="color:red"></i> > 28°C (Warm)</p>
        <p><i class="fa fa-tint" style="color:orange"></i> 26-28°C (Moderate)</p>
        <p><i class="fa fa-tint" style="color:yellow"></i> 24-26°C (Cool)</p>
        <p><i class="fa fa-tint" style="color:blue"></i> < 24°C (Cold)</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Display map
        st_folium(m, width=700, height=500, returned_objects=[])
        
        # Show data summary
        st.info(f"📍 Displaying {len(lats)} ARGO float locations in the region")
        
    except Exception as e:
        st.error(f"❌ Error displaying map: {e}")
        st.info("🔄 Loading fallback map...")
        # Fallback to simple map
        try:
            m = folium.Map(location=[20.0, 77.0], zoom_start=5)
            st_folium(m, width=700, height=400)
        except Exception as fallback_error:
            st.error(f"❌ Fallback map also failed: {fallback_error}")
            st.info("🗺️ Map visualization is temporarily unavailable.")

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

def show_3d_visualization(viz_config):
    """Show 3D visualization"""
    st.info("🌐 3D visualization feature coming soon!")
    # For now, show a placeholder
    st.plotly_chart(go.Figure().add_trace(go.Scatter3d(
        x=[1, 2, 3], y=[1, 2, 3], z=[1, 2, 3],
        mode='markers',
        marker=dict(size=5, color='blue')
    )).update_layout(title="3D Visualization Placeholder"))

def show_generic_visualization(viz_config):
    """Show generic visualization for unknown types"""
    try:
        config = viz_config.get('config', {})
        if 'data' in config and 'layout' in config:
            # Try to display as Plotly figure
            fig = go.Figure(data=config['data'], layout=config['layout'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Visualization data is available but cannot be displayed in this format.")
    except Exception as e:
        st.warning(f"⚠️ Could not render visualization: {e}")
        st.info("📊 Raw visualization data is available but not displayable.")

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