#!/usr/bin/env python3
"""
Simple test script for Render deployment verification
"""

import os
import sys
import time
import requests
import json
import threading
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
        
        fast_service = FastDataService()
        viz_service = VisualizationService()
        
        print("Service initialization successful")
        return True
        
    except Exception as e:
        print(f"Backend startup failed: {e}")
        return False

def test_real_time_data():
    """Test real-time data fetching"""
    print("Testing real-time data fetching...")
    
    try:
        from backend.services.fast_data_service import FastDataService
        
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
            print(f"Real-time data fetch successful: {result.record_count} records")
            print(f"Variables: {result.summary.variables}")
            return True
        else:
            print("No data returned from real-time fetch")
            return False
            
    except Exception as e:
        print(f"Real-time data test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("Testing environment variables...")
    
    required_vars = ['APP_NAME', 'APP_VERSION', 'DEBUG']
    optional_vars = ['GROQ_API_KEY', 'COHERE_API_KEY', 'PINECONE_API_KEY']
    
    # Check required variables
    for var in required_vars:
        if os.getenv(var):
            print(f"{var}: {os.getenv(var)}")
        else:
            print(f"{var}: Not set (using default)")
    
    # Check optional variables
    api_keys_found = 0
    for var in optional_vars:
        if os.getenv(var) and os.getenv(var) != f"your_{var.lower()}_here":
            print(f"{var}: Set")
            api_keys_found += 1
        else:
            print(f"{var}: Not set")
    
    if api_keys_found == 0:
        print("No API keys found - using mock data mode")
    else:
        print(f"{api_keys_found} API keys configured")
    
    return True

def main():
    """Run all tests"""
    print("FloatChat Render Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Backend Startup", test_backend_startup),
        ("Real-time Data", test_real_time_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} Test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Your deployment is ready for Render!")
    elif passed >= total * 0.8:
        print("Most tests passed. Review failed tests before deployment.")
    else:
        print("Multiple tests failed. Please fix issues before deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
