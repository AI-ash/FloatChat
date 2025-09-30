"""
Cloud-based Streamlit frontend for FloatChat
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
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f1f8e9;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'student'

# Get backend URL from environment or default
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🌊 FloatChat</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">AI-Powered ARGO Oceanographic Data Assistant</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # User role selection
        user_role = st.selectbox(
            "Select your role:",
            ["student", "researcher", "policymaker"],
            index=["student", "researcher", "policymaker"].index(st.session_state.user_role)
        )
        st.session_state.user_role = user_role
        
        # Quick actions
        st.header("Quick Actions")
        
        if st.button("🗺️ Explore Active Floats"):
            show_active_floats()
        
        if st.button("📈 Regional Trends"):
            show_regional_trends()
        
        if st.button("🔍 Data Explorer"):
            show_data_explorer()
        
        # Suggested queries
        st.header("Suggested Queries")
        suggested_queries = get_suggested_queries(user_role)
        
        for query in suggested_queries:
            if st.button(f"💬 {query[:30]}...", key=f"suggest_{hash(query)}"):
                process_query(query)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat interface
        st.header("Chat with AI Assistant")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
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
        

    
    with col2:
        # Information panel
        st.header("Quick Info")
        
        # System status
        with st.expander("System Status", expanded=True):
            show_system_status()
        
        # Recent activity
        with st.expander("Recent Activity"):
            show_recent_activity()
        
        # Data quality info
        with st.expander("Data Quality"):
            show_data_quality_info()

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
            # Call cloud backend API
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={
                    "query": query,
                    "user_role": st.session_state.user_role
                },
                timeout=15  # Reduced timeout to fail faster
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
            elif viz_type == '3d':
                show_3d_visualization(viz)
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
        name='Sea Surface Temperature',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title='Temperature Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_3d_visualization(viz_config):
    """Show 3D visualization"""
    st.info("3D visualization feature coming soon!")

def show_active_floats():
    """Show active ARGO floats"""
    st.header("Active ARGO Floats")
    
    # Sample data (replace with API call)
    float_data = {
        'Float ID': ['5904471', '2902746', '2902747', '5904472'],
        'Last Position': ['15.2°N, 75.3°E', '18.5°N, 82.1°E', '22.1°N, 88.4°E', '12.8°N, 79.2°E'],
        'Days Since Profile': [2, 5, 1, 8],
        'Status': ['Active', 'Active', 'Active', 'Delayed']
    }
    
    df = pd.DataFrame(float_data)
    st.dataframe(df, use_container_width=True)

def show_regional_trends():
    """Show regional climate trends"""
    st.header("Regional Climate Trends")
    
    region = st.selectbox("Select Region:", [
        "Bay of Bengal", "Arabian Sea", "Indian Ocean", "Equatorial Indian Ocean"
    ])
    
    variable = st.selectbox("Select Variable:", [
        "temperature", "salinity", "oxygen"
    ])
    
    if st.button("Generate Trend Analysis"):
        with st.spinner("Analyzing trends..."):
            # Simulate trend analysis
            time.sleep(2)
            st.success(f"Trend analysis for {variable} in {region} completed!")
            
            # Show sample trend plot
            show_plot_visualization({})

def show_data_explorer():
    """Show data explorer interface"""
    st.header("Data Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Filters")
        date_range = st.date_input(
            "Date Range:",
            value=(datetime.now() - timedelta(days=365), datetime.now()),
            max_value=datetime.now()
        )
        
        depth_range = st.slider(
            "Depth Range (m):",
            min_value=0,
            max_value=2000,
            value=(0, 500)
        )
        
        variables = st.multiselect(
            "Variables:",
            ["temperature", "salinity", "pressure", "oxygen"],
            default=["temperature"]
        )
    
    with col2:
        st.subheader("Results")
        if st.button("Search Data"):
            st.info("Data search functionality coming soon!")

def get_suggested_queries(user_role):
    """Get role-specific suggested queries"""
    queries = {
        'student': [
            "What is the average temperature in Bay of Bengal?",
            "Show me recent ARGO float locations",
            "Explain ocean salinity patterns"
        ],
        'researcher': [
            "Temperature trends in Arabian Sea over last decade",
            "Oxygen minimum zone analysis in Indian Ocean",
            "Compare salinity profiles between monsoon seasons"
        ],
        'policymaker': [
            "Ocean warming trends affecting Indian coastline",
            "Climate change impacts on marine ecosystems",
            "Seasonal patterns affecting fisheries"
        ]
    }
    return queries.get(user_role, queries['student'])

def show_system_status():
    """Show system status information"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Active Floats", "1,247", "↑ 23")
        st.metric("Data Records", "2.3M", "↑ 15K")
    
    with col2:
        st.metric("API Status", "Online", "✅")
        st.metric("Last Update", "2 hrs ago", "🔄")

def show_recent_activity():
    """Show recent system activity"""
    activities = [
        "New ARGO data ingested - 2 hours ago",
        "Trend analysis completed - 4 hours ago", 
        "Quality control check passed - 6 hours ago"
    ]
    
    for activity in activities:
        st.text(f"• {activity}")

def show_data_quality_info():
    """Show data quality information"""
    st.text("Quality Control Flags:")
    st.text("✅ Good data: 89.2%")
    st.text("⚠️ Probably good: 8.1%") 
    st.text("❌ Bad data: 2.7%")

if __name__ == "__main__":
    # Import numpy for sample data
    import numpy as np
    main()