<<<<<<< HEAD
#!/usr/bin/env python3
"""
Test the frontend visualization fix
"""

import requests
import json

def test_frontend_query():
    """Test a query that would trigger visualizations"""
    
    print("🧪 Testing Frontend Visualization Fix")
    print("=" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Test query that should generate visualizations
    query_data = {
        "query": "Show me ARGO float locations in Bay of Bengal with temperature data",
        "user_role": "student"
    }
    
    try:
        print("🔍 Sending query to backend...")
        response = requests.post(
            f"{backend_url}/api/query",
            json=query_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query successful!")
            print(f"📊 Response: {data.get('response', '')[:100]}...")
            print(f"📈 Data records: {data.get('data_summary', {}).get('record_count', 0)}")
            
            # Check visualizations
            visualizations = data.get('visualizations', [])
            print(f"🎨 Visualizations: {len(visualizations)}")
            
            for i, viz in enumerate(visualizations):
                print(f"   {i+1}. Type: {viz.get('type', 'unknown')}")
                print(f"      Title: {viz.get('title', 'No title')}")
                
                # Check if config is serializable
                config = viz.get('config', {})
                try:
                    json.dumps(config)
                    print(f"      Config: ✅ JSON serializable")
                except Exception as e:
                    print(f"      Config: ❌ Not serializable - {e}")
            
            print("\n✅ Frontend should now handle this data correctly!")
            print("🌊 Try running the query in the Streamlit interface")
            
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Test the frontend visualization fix
"""

import requests
import json

def test_frontend_query():
    """Test a query that would trigger visualizations"""
    
    print("🧪 Testing Frontend Visualization Fix")
    print("=" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Test query that should generate visualizations
    query_data = {
        "query": "Show me ARGO float locations in Bay of Bengal with temperature data",
        "user_role": "student"
    }
    
    try:
        print("🔍 Sending query to backend...")
        response = requests.post(
            f"{backend_url}/api/query",
            json=query_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query successful!")
            print(f"📊 Response: {data.get('response', '')[:100]}...")
            print(f"📈 Data records: {data.get('data_summary', {}).get('record_count', 0)}")
            
            # Check visualizations
            visualizations = data.get('visualizations', [])
            print(f"🎨 Visualizations: {len(visualizations)}")
            
            for i, viz in enumerate(visualizations):
                print(f"   {i+1}. Type: {viz.get('type', 'unknown')}")
                print(f"      Title: {viz.get('title', 'No title')}")
                
                # Check if config is serializable
                config = viz.get('config', {})
                try:
                    json.dumps(config)
                    print(f"      Config: ✅ JSON serializable")
                except Exception as e:
                    print(f"      Config: ❌ Not serializable - {e}")
            
            print("\n✅ Frontend should now handle this data correctly!")
            print("🌊 Try running the query in the Streamlit interface")
            
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    test_frontend_query()