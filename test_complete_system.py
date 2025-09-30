#!/usr/bin/env python3
"""
Test the complete FloatChat system
"""

import requests
import json
import time

def test_system():
    """Test the complete system"""
    
    print("🧪 Testing Complete FloatChat System")
    print("=" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("🔍 Test 1: Backend Health Check")
    try:
        response = requests.get(f"{backend_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            data = response.json()
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python run_floatchat.py")
        return False
    
    # Test 2: Test endpoint
    print("\n🔍 Test 2: DataSummary Serialization")
    try:
        response = requests.get(f"{backend_url}/test", timeout=5)
        if response.status_code == 200:
            print("✅ DataSummary serialization works")
            data = response.json()
            print(f"   Record count: {data.get('record_count', 0)}")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Test endpoint error: {e}")
    
    # Test 3: Query processing
    print("\n🔍 Test 3: Query Processing")
    try:
        query_data = {
            "query": "Show me temperature data in Bay of Bengal",
            "user_role": "student"
        }
        
        response = requests.post(
            f"{backend_url}/api/query",
            json=query_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Query processing works")
            data = response.json()
            print(f"   Response: {data.get('response', '')[:100]}...")
            print(f"   Data records: {data.get('data_summary', {}).get('record_count', 0)}")
            print(f"   Data sources: {data.get('data_summary', {}).get('data_sources', [])}")
        else:
            print(f"❌ Query processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Query processing error: {e}")
    
    # Test 4: Available variables
    print("\n🔍 Test 4: Available Variables")
    try:
        response = requests.get(f"{backend_url}/api/data/variables", timeout=5)
        if response.status_code == 200:
            print("✅ Variables endpoint works")
            data = response.json()
            print(f"   Available variables: {data}")
        else:
            print(f"❌ Variables endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Variables endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 System test completed!")
    print("💡 If all tests pass, FloatChat is working correctly")
    print("🌊 Open http://localhost:8501 to use the interface")
    print("=" * 50)

if __name__ == "__main__":
    test_system()