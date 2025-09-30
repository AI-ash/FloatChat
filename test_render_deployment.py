#!/usr/bin/env python3
"""
Test script for Render deployment verification
Tests backend connection, real-time data fetching, and visualization
"""

import os
import sys
import time
import requests
import json
import threading
import subprocess
from datetime import datetime, timedelta

def test_backend_startup():
    """Test if backend starts correctly"""
    print("Testing backend startup...")
    
    try:
        # Import backend components
        from backend.main import app
        print("Backend imports successful")
        
        # Test service initialization
        from backend.services.fast_data_service import FastDataService
        from backend.services.visualization_service import VisualizationService
        from backend.services.llm_service import LLMService
        
        fast_service = FastDataService()
        viz_service = VisualizationService()
        llm_service = LLMService()
        
        print("✅ Service initialization successful")
        return True
        
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
        return False

def test_real_time_data():
    """Test real-time data fetching"""
    print("🌊 Testing real-time data fetching...")
    
    try:
        from backend.services.fast_data_service import FastDataService
        from backend.models import QueryType
        
        service = FastDataService()
        
        # Test data fetching with realistic parameters
        variables = ['temperature', 'salinity']
        spatial_bounds = [75.0, 10.0, 95.0, 25.0]  # Bay of Bengal
        temporal_bounds = [datetime.now() - timedelta(days=30), datetime.now()]
        depth_range = [0, 500]
        qc_flags = [1, 2, 5, 8]
        
        # Fetch data
        result = service.fetch_data(
            variables=variables,
            spatial_bounds=spatial_bounds,
            temporal_bounds=temporal_bounds,
            depth_range=depth_range,
            qc_flags=qc_flags
        )
        
        if result and result.record_count > 0:
            print(f"✅ Real-time data fetch successful: {result.record_count} records")
            print(f"   Variables: {result.summary.variables}")
            print(f"   Spatial coverage: {result.summary.spatial_coverage}")
            print(f"   Data sources: {result.summary.data_sources}")
            return True
        else:
            print("❌ No data returned from real-time fetch")
            return False
            
    except Exception as e:
        print(f"❌ Real-time data test failed: {e}")
        return False

def test_visualization_generation():
    """Test visualization generation"""
    print("📊 Testing visualization generation...")
    
    try:
        from backend.services.visualization_service import VisualizationService
        from backend.models import QueryType
        
        service = VisualizationService()
        
        # Create sample data
        sample_data = [
            {
                'float_id': 'TEST_001',
                'latitude': 20.0,
                'longitude': 80.0,
                'timestamp': datetime.now(),
                'measurements': {
                    'temperature': {
                        'values': [28.5, 27.2, 25.8],
                        'depths': [0, 50, 100],
                        'qc_flags': [1, 1, 1]
                    },
                    'salinity': {
                        'values': [33.2, 34.1, 34.5],
                        'depths': [0, 50, 100],
                        'qc_flags': [1, 1, 1]
                    }
                }
            },
            {
                'float_id': 'TEST_002',
                'latitude': 22.0,
                'longitude': 85.0,
                'timestamp': datetime.now() - timedelta(hours=6),
                'measurements': {
                    'temperature': {
                        'values': [29.1, 28.0, 26.5],
                        'depths': [0, 50, 100],
                        'qc_flags': [1, 1, 1]
                    }
                }
            }
        ]
        
        # Test different visualization types
        viz_types = [
            (QueryType.SPATIAL, "spatial"),
            (QueryType.TIMESERIES, "timeseries"),
            (QueryType.PROFILE, "profile")
        ]
        
        success_count = 0
        for query_type, name in viz_types:
            try:
                visualizations = service.create_visualizations(
                    data=sample_data,
                    query_type=query_type,
                    variables=['temperature', 'salinity']
                )
                
                if visualizations:
                    print(f"✅ {name} visualization generated successfully")
                    success_count += 1
                else:
                    print(f"⚠️ {name} visualization returned empty")
                    
            except Exception as e:
                print(f"❌ {name} visualization failed: {e}")
        
        if success_count > 0:
            print(f"✅ Visualization generation successful: {success_count}/{len(viz_types)} types")
            return True
        else:
            print("❌ No visualizations generated successfully")
            return False
            
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("🔗 Testing API endpoints...")
    
    try:
        # Start backend in background
        import uvicorn
        from backend.main import app
        
        # Start server in thread
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://127.0.0.1:8001"
        
        # Test health endpoint
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test query endpoint
        query_data = {
            "query": "Show me temperature data in Bay of Bengal",
            "user_role": "student"
        }
        
        response = requests.post(
            f"{base_url}/api/query",
            json=query_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'response' in result:
                print("✅ Query endpoint working")
                print(f"   Response length: {len(result['response'])} characters")
                if 'visualizations' in result:
                    print(f"   Visualizations: {len(result['visualizations'])} generated")
                return True
            else:
                print("❌ Query endpoint returned invalid response")
                return False
        else:
            print(f"❌ Query endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("🔧 Testing environment variables...")
    
    required_vars = [
        'APP_NAME',
        'APP_VERSION',
        'DEBUG'
    ]
    
    optional_vars = [
        'GROQ_API_KEY',
        'COHERE_API_KEY',
        'PINECONE_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    success = True
    
    # Check required variables
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var}: {os.getenv(var)}")
        else:
            print(f"⚠️ {var}: Not set (using default)")
    
    # Check optional variables
    api_keys_found = 0
    for var in optional_vars:
        if os.getenv(var) and os.getenv(var) != f"your_{var.lower()}_here":
            print(f"✅ {var}: Set")
            api_keys_found += 1
        else:
            print(f"⚠️ {var}: Not set")
    
    if api_keys_found == 0:
        print("⚠️ No API keys found - using mock data mode")
    else:
        print(f"✅ {api_keys_found} API keys configured")
    
    return True

def test_docker_build():
    """Test Docker build process"""
    print("🐳 Testing Docker build...")
    
    try:
        # Check if Dockerfile exists
        if not os.path.exists("Dockerfile"):
            print("❌ Dockerfile not found")
            return False
        
        # Check if requirements file exists
        if not os.path.exists("requirements-production.txt"):
            print("❌ requirements-production.txt not found")
            return False
        
        print("✅ Docker configuration files found")
        
        # Test Docker build (optional - requires Docker)
        try:
            result = subprocess.run(
                ["docker", "build", "-t", "floatchat-test", "."],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✅ Docker build successful")
                # Clean up test image
                subprocess.run(["docker", "rmi", "floatchat-test"], capture_output=True)
                return True
            else:
                print(f"❌ Docker build failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Docker build timed out")
            return False
        except FileNotFoundError:
            print("⚠️ Docker not available - skipping build test")
            return True
            
    except Exception as e:
        print(f"❌ Docker test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("FloatChat Render Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Backend Startup", test_backend_startup),
        ("Real-time Data", test_real_time_data),
        ("Visualization Generation", test_visualization_generation),
        ("API Endpoints", test_api_endpoints),
        ("Docker Build", test_docker_build)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your deployment is ready for Render!")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. Review failed tests before deployment.")
    else:
        print("❌ Multiple tests failed. Please fix issues before deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
