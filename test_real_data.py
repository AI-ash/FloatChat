<<<<<<< HEAD
#!/usr/bin/env python3
"""
Test the real data service
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.real_data_service import RealDataService
from datetime import datetime, timedelta

async def test_real_data_service():
    """Test the real data service"""
    
    print("🌊 Testing Real Data Service")
    print("=" * 40)
    
    service = RealDataService()
    
    try:
        await service.initialize()
        print("✅ Service initialized")
        
        # Test data fetch
        variables = ['temperature', 'salinity']
        spatial_bounds = [70.0, 10.0, 90.0, 25.0]  # Bay of Bengal area
        temporal_bounds = [
            datetime.now() - timedelta(days=7),
            datetime.now()
        ]
        depth_range = [0.0, 100.0]
        qc_flags = [1]
        
        print(f"🔍 Fetching data for: {variables}")
        print(f"📍 Area: {spatial_bounds}")
        
        result = await service.fetch_data(
            variables=variables,
            spatial_bounds=spatial_bounds,
            temporal_bounds=temporal_bounds,
            depth_range=depth_range,
            qc_flags=qc_flags
        )
        
        print(f"✅ Got {result.record_count} records")
        print(f"📊 Data sources: {result.summary.data_sources}")
        print(f"🎯 Variables: {result.summary.variables}")
        
        if result.data:
            sample = result.data[0]
            print(f"📝 Sample record: Float {sample.get('float_id', 'Unknown')}")
            print(f"📍 Location: {sample.get('latitude', 0):.2f}, {sample.get('longitude', 0):.2f}")
            
            measurements = sample.get('measurements', {})
            for var, data in measurements.items():
                values = data.get('values', [])
                if values:
                    print(f"🌡️ {var.title()}: {values[0]:.2f}")
        
        print("✅ Real data service test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await service.close()
        print("🔧 Service closed")

if __name__ == "__main__":
=======
#!/usr/bin/env python3
"""
Test the real data service
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.real_data_service import RealDataService
from datetime import datetime, timedelta

async def test_real_data_service():
    """Test the real data service"""
    
    print("🌊 Testing Real Data Service")
    print("=" * 40)
    
    service = RealDataService()
    
    try:
        await service.initialize()
        print("✅ Service initialized")
        
        # Test data fetch
        variables = ['temperature', 'salinity']
        spatial_bounds = [70.0, 10.0, 90.0, 25.0]  # Bay of Bengal area
        temporal_bounds = [
            datetime.now() - timedelta(days=7),
            datetime.now()
        ]
        depth_range = [0.0, 100.0]
        qc_flags = [1]
        
        print(f"🔍 Fetching data for: {variables}")
        print(f"📍 Area: {spatial_bounds}")
        
        result = await service.fetch_data(
            variables=variables,
            spatial_bounds=spatial_bounds,
            temporal_bounds=temporal_bounds,
            depth_range=depth_range,
            qc_flags=qc_flags
        )
        
        print(f"✅ Got {result.record_count} records")
        print(f"📊 Data sources: {result.summary.data_sources}")
        print(f"🎯 Variables: {result.summary.variables}")
        
        if result.data:
            sample = result.data[0]
            print(f"📝 Sample record: Float {sample.get('float_id', 'Unknown')}")
            print(f"📍 Location: {sample.get('latitude', 0):.2f}, {sample.get('longitude', 0):.2f}")
            
            measurements = sample.get('measurements', {})
            for var, data in measurements.items():
                values = data.get('values', [])
                if values:
                    print(f"🌡️ {var.title()}: {values[0]:.2f}")
        
        print("✅ Real data service test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await service.close()
        print("🔧 Service closed")

if __name__ == "__main__":
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    asyncio.run(test_real_data_service())