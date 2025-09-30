#!/usr/bin/env python3
"""
Test visualization serialization fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import asyncio
from backend.services.visualization_service import VisualizationService
from backend.models import QueryType
from datetime import datetime

async def test_visualization_serialization():
    """Test that visualizations are properly serializable"""
    
    print("🧪 Testing Visualization Serialization")
    print("=" * 50)
    
    viz_service = VisualizationService()
    await viz_service.initialize()
    
    # Create sample data
    sample_data = [
        {
            'float_id': 'TEST_001',
            'latitude': 15.5,
            'longitude': 75.2,
            'timestamp': datetime.now(),
            'measurements': {
                'temperature': {
                    'values': [28.5],
                    'depths': [0.0],
                    'qc_flags': [1]
                }
            }
        },
        {
            'float_id': 'TEST_002',
            'latitude': 18.0,
            'longitude': 82.0,
            'timestamp': datetime.now(),
            'measurements': {
                'temperature': {
                    'values': [27.8],
                    'depths': [0.0],
                    'qc_flags': [1]
                }
            }
        }
    ]
    
    try:
        # Test map visualization
        print("🗺️ Testing map visualization...")
        visualizations = await viz_service.create_visualizations(
            data=sample_data,
            query_type=QueryType.SPATIAL,
            variables=['temperature']
        )
        
        print(f"✅ Created {len(visualizations)} visualizations")
        
        for i, viz in enumerate(visualizations):
            print(f"\n📊 Visualization {i+1}:")
            print(f"   Type: {viz.type}")
            print(f"   Title: {viz.title}")
            
            # Test JSON serialization
            try:
                # Convert to dict first
                viz_dict = {
                    'type': viz.type,
                    'title': viz.title,
                    'config': viz.config,
                    'data_url': viz.data_url,
                    'thumbnail_url': viz.thumbnail_url
                }
                
                # Test JSON serialization
                json_str = json.dumps(viz_dict, default=str)
                print("   ✅ JSON serializable")
                
                # Test deserialization
                parsed = json.loads(json_str)
                print("   ✅ JSON deserializable")
                
                # Check config structure
                config = viz.config
                if 'data' in config and config['data']:
                    data_config = config['data'][0]
                    print(f"   📍 Locations: {len(data_config.get('lat', []))}")
                    print(f"   🌡️ Values: {len(data_config.get('color', []))}")
                
            except Exception as e:
                print(f"   ❌ Serialization error: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n🎉 Visualization serialization test completed!")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_visualization_serialization())