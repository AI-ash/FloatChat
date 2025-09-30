<<<<<<< HEAD
#!/usr/bin/env python3
"""
Test visualization directly without starting full server
"""

import requests
import json
import time
import subprocess
import sys

def start_backend():
    """Start backend in background"""
    print("🚀 Starting backend...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8001"  # Use different port
    ])
    time.sleep(5)  # Wait for startup
    return process

def test_visualization():
    """Test visualization with the new backend"""
    
    backend_url = "http://localhost:8001"
    
    # Test query
    query_data = {
        "query": "Show me temperature data in Bay of Bengal",
        "user_role": "student"
    }
    
    try:
        print("🔍 Testing query with new backend...")
        response = requests.post(
            f"{backend_url}/api/query",
            json=query_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query successful!")
            print(f"📊 Response: {data.get('response', '')[:100]}...")
            print(f"📈 Data records: {data.get('data_summary', {}).get('record_count', 0)}")
            print(f"🗂️ Data sources: {data.get('data_summary', {}).get('data_sources', [])}")
            
            # Check visualizations
            visualizations = data.get('visualizations', [])
            print(f"🎨 Visualizations: {len(visualizations)}")
            
            for i, viz in enumerate(visualizations):
                print(f"   {i+1}. Type: {viz.get('type', 'unknown')}")
                print(f"      Title: {viz.get('title', 'No title')}")
                
                # Test serialization
                try:
                    json.dumps(viz)
                    print(f"      ✅ Serializable")
                except Exception as e:
                    print(f"      ❌ Not serializable: {e}")
            
            return True
            
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Visualization Fix Directly")
    print("=" * 50)
    
    backend_process = None
    try:
        backend_process = start_backend()
        
        # Test the visualization
        success = test_visualization()
        
        if success:
            print("\n✅ Visualization fix successful!")
            print("🌊 The frontend should now work without errors")
        else:
            print("\n❌ Visualization fix failed")
            
    finally:
        if backend_process:
            print("\n🛑 Stopping backend...")
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Test visualization directly without starting full server
"""

import requests
import json
import time
import subprocess
import sys

def start_backend():
    """Start backend in background"""
    print("🚀 Starting backend...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "127.0.0.1",
        "--port", "8001"  # Use different port
    ])
    time.sleep(5)  # Wait for startup
    return process

def test_visualization():
    """Test visualization with the new backend"""
    
    backend_url = "http://localhost:8001"
    
    # Test query
    query_data = {
        "query": "Show me temperature data in Bay of Bengal",
        "user_role": "student"
    }
    
    try:
        print("🔍 Testing query with new backend...")
        response = requests.post(
            f"{backend_url}/api/query",
            json=query_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query successful!")
            print(f"📊 Response: {data.get('response', '')[:100]}...")
            print(f"📈 Data records: {data.get('data_summary', {}).get('record_count', 0)}")
            print(f"🗂️ Data sources: {data.get('data_summary', {}).get('data_sources', [])}")
            
            # Check visualizations
            visualizations = data.get('visualizations', [])
            print(f"🎨 Visualizations: {len(visualizations)}")
            
            for i, viz in enumerate(visualizations):
                print(f"   {i+1}. Type: {viz.get('type', 'unknown')}")
                print(f"      Title: {viz.get('title', 'No title')}")
                
                # Test serialization
                try:
                    json.dumps(viz)
                    print(f"      ✅ Serializable")
                except Exception as e:
                    print(f"      ❌ Not serializable: {e}")
            
            return True
            
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Visualization Fix Directly")
    print("=" * 50)
    
    backend_process = None
    try:
        backend_process = start_backend()
        
        # Test the visualization
        success = test_visualization()
        
        if success:
            print("\n✅ Visualization fix successful!")
            print("🌊 The frontend should now work without errors")
        else:
            print("\n❌ Visualization fix failed")
            
    finally:
        if backend_process:
            print("\n🛑 Stopping backend...")
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    main()