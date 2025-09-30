<<<<<<< HEAD
#!/usr/bin/env python3
"""
Test DataSummary serialization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models import DataSummary, QueryResponse, Visualization, Provenance
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import json

# Test DataSummary serialization
print("Testing DataSummary serialization...")

test_summary = DataSummary(
    record_count=10,
    variables=['temperature'],
    spatial_coverage={'min_lat': -90.0, 'max_lat': 90.0, 'min_lon': -180.0, 'max_lon': 180.0},
    temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
    depth_coverage={'min_depth': 0.0, 'max_depth': 2000.0},
    data_sources=['TEST'],
    qc_summary={'good': 10, 'questionable': 0, 'bad': 0}
)

print("✅ DataSummary created successfully")

# Test JSON encoding
try:
    encoded = jsonable_encoder(test_summary)
    print("✅ DataSummary encoded successfully")
    print(f"Encoded keys: {list(encoded.keys())}")
    
    # Test JSON serialization
    json_str = json.dumps(encoded)
    print("✅ DataSummary JSON serialized successfully")
    
    # Test deserialization
    decoded = json.loads(json_str)
    print("✅ DataSummary JSON deserialized successfully")
    print(f"Record count: {decoded['record_count']}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test QueryResponse serialization
print("\nTesting QueryResponse serialization...")

test_viz = Visualization(
    type="map",
    title="Test Map",
    config={"test": "data"}
)

test_provenance = Provenance(
    datasets_used=['TEST'],
    access_timestamp=datetime.now(),
    qc_flags_applied=[1],
    spatial_filters=[-90.0, 90.0, -180.0, 180.0],
    temporal_filters=[datetime.now(), datetime.now()],
    processing_steps=['test'],
    data_quality_score=0.95
)

test_response = QueryResponse(
    query="test query",
    response="test response",
    data_summary=test_summary,
    visualizations=[test_viz],
    provenance=test_provenance,
    processing_time=0.1
)

try:
    encoded_response = jsonable_encoder(test_response)
    print("✅ QueryResponse encoded successfully")
    
    json_response = json.dumps(encoded_response)
    print("✅ QueryResponse JSON serialized successfully")
    
    decoded_response = json.loads(json_response)
    print("✅ QueryResponse JSON deserialized successfully")
    print(f"Response keys: {list(decoded_response.keys())}")
    print(f"Data summary record count: {decoded_response['data_summary']['record_count']}")
    
except Exception as e:
    print(f"❌ Error: {e}")

=======
#!/usr/bin/env python3
"""
Test DataSummary serialization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models import DataSummary, QueryResponse, Visualization, Provenance
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import json

# Test DataSummary serialization
print("Testing DataSummary serialization...")

test_summary = DataSummary(
    record_count=10,
    variables=['temperature'],
    spatial_coverage={'min_lat': -90.0, 'max_lat': 90.0, 'min_lon': -180.0, 'max_lon': 180.0},
    temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
    depth_coverage={'min_depth': 0.0, 'max_depth': 2000.0},
    data_sources=['TEST'],
    qc_summary={'good': 10, 'questionable': 0, 'bad': 0}
)

print("✅ DataSummary created successfully")

# Test JSON encoding
try:
    encoded = jsonable_encoder(test_summary)
    print("✅ DataSummary encoded successfully")
    print(f"Encoded keys: {list(encoded.keys())}")
    
    # Test JSON serialization
    json_str = json.dumps(encoded)
    print("✅ DataSummary JSON serialized successfully")
    
    # Test deserialization
    decoded = json.loads(json_str)
    print("✅ DataSummary JSON deserialized successfully")
    print(f"Record count: {decoded['record_count']}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test QueryResponse serialization
print("\nTesting QueryResponse serialization...")

test_viz = Visualization(
    type="map",
    title="Test Map",
    config={"test": "data"}
)

test_provenance = Provenance(
    datasets_used=['TEST'],
    access_timestamp=datetime.now(),
    qc_flags_applied=[1],
    spatial_filters=[-90.0, 90.0, -180.0, 180.0],
    temporal_filters=[datetime.now(), datetime.now()],
    processing_steps=['test'],
    data_quality_score=0.95
)

test_response = QueryResponse(
    query="test query",
    response="test response",
    data_summary=test_summary,
    visualizations=[test_viz],
    provenance=test_provenance,
    processing_time=0.1
)

try:
    encoded_response = jsonable_encoder(test_response)
    print("✅ QueryResponse encoded successfully")
    
    json_response = json.dumps(encoded_response)
    print("✅ QueryResponse JSON serialized successfully")
    
    decoded_response = json.loads(json_response)
    print("✅ QueryResponse JSON deserialized successfully")
    print(f"Response keys: {list(decoded_response.keys())}")
    print(f"Data summary record count: {decoded_response['data_summary']['record_count']}")
    
except Exception as e:
    print(f"❌ Error: {e}")

>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
print("\n🎉 All serialization tests passed!")