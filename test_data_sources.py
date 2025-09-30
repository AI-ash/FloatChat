#!/usr/bin/env python3
"""
Test real oceanographic data sources
"""

import requests
import json
from datetime import datetime, timedelta

def test_argo_sources():
    """Test various ARGO data sources"""
    
    print("🌊 Testing Real Oceanographic Data Sources")
    print("=" * 50)
    
    # Test sources
    sources = {
        "ARGO Global Data Assembly Centre": "https://www.argodatamgt.org/Access-to-data/Argo-GDAC-ftp-and-https-servers",
        "IFREMER ERDDAP": "https://www.ifremer.fr/erddap/tabledap/ArgoFloats.json?longitude,latitude,time,temp&time>=2024-01-01",
        "NOAA ERDDAP": "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/argo_all.json?longitude,latitude,time,temp&time>=2024-01-01&longitude>70&longitude<90&latitude>10&latitude<25",
        "Copernicus Marine": "https://marine.copernicus.eu/",
        "ARGO Float Data": "https://argo.ucsd.edu/data/",
    }
    
    for name, url in sources.items():
        print(f"\n🔍 Testing {name}:")
        print(f"URL: {url}")
        
        try:
            if url.endswith('.json'):
                response = requests.get(url, timeout=10)
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success! Got {len(data.get('table', {}).get('rows', []))} records")
                else:
                    print(f"❌ Failed: {response.text[:200]}")
            else:
                response = requests.head(url, timeout=10)
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    print("✅ Accessible")
                else:
                    print("❌ Not accessible")
                    
        except Exception as e:
            print(f"❌ Error: {e}")

def test_alternative_sources():
    """Test alternative oceanographic data sources"""
    
    print("\n🌊 Testing Alternative Data Sources")
    print("=" * 50)
    
    # Alternative sources that might be more accessible
    alt_sources = {
        "World Ocean Database": "https://www.ncei.noaa.gov/data/oceans/woa/",
        "Global Temperature Anomaly": "https://www.ncei.noaa.gov/data/global-summary-of-the-month/access/",
        "Ocean Color Data": "https://oceancolor.gsfc.nasa.gov/",
        "GEBCO Bathymetry": "https://www.gebco.net/data_and_products/gridded_bathymetry_data/",
    }
    
    for name, url in alt_sources.items():
        print(f"\n🔍 Testing {name}:")
        try:
            response = requests.head(url, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ Accessible")
            else:
                print("❌ Not accessible")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_simple_ocean_api():
    """Test a simple ocean data API"""
    
    print("\n🌊 Testing Simple Ocean APIs")
    print("=" * 50)
    
    # Try some simpler APIs
    simple_apis = {
        "OpenWeatherMap Ocean": "https://api.openweathermap.org/data/2.5/weather?lat=15&lon=75&appid=demo",
        "Marine Weather": "https://marine-api.open-meteo.com/v1/marine?latitude=15&longitude=75&hourly=wave_height,wave_direction,wave_period",
        "Tide API": "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station=8518750&product=water_level&datum=MLLW&time_zone=gmt&units=metric&format=json",
    }
    
    for name, url in simple_apis.items():
        print(f"\n🔍 Testing {name}:")
        try:
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Sample data: {str(data)[:200]}...")
            else:
                print(f"❌ Failed: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_argo_sources()
    test_alternative_sources() 
    test_simple_ocean_api()
    
    print("\n" + "=" * 50)
    print("🎯 Recommendations:")
    print("1. Use mock data for demonstration")
    print("2. Implement Marine Weather API for real data")
    print("3. Add NOAA Tides API for coastal data")
    print("4. Consider OpenWeatherMap Marine for weather data")
    print("=" * 50)