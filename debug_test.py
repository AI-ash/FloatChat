<<<<<<< HEAD
#!/usr/bin/env python3
"""
Debug test to check DataSummary serialization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models import DataSummary
from datetime import datetime
import json

# Create a test DataSummary
test_summary = DataSummary(
    record_count=100,
    variables=['temperature', 'salinity'],
    spatial_coverage={'min_lat': -90, 'max_lat': 90, 'min_lon': -180, 'max_lon': 180},
    temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
    depth_coverage={'min_depth': 0, 'max_depth': 2000},
    data_sources=['ARGO'],
    qc_summary={'good': 90, 'questionable': 10}
)

print("DataSummary object:")
print(test_summary)
print("\nDataSummary dict:")
print(test_summary.dict())
print("\nDataSummary JSON:")
print(test_summary.json())

# Test if it has get method
print(f"\nHas 'get' method: {hasattr(test_summary, 'get')}")
print(f"Record count via attribute: {test_summary.record_count}")

try:
    print(f"Record count via get: {test_summary.get('record_count', 0)}")
except AttributeError as e:
=======
#!/usr/bin/env python3
"""
Debug test to check DataSummary serialization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models import DataSummary
from datetime import datetime
import json

# Create a test DataSummary
test_summary = DataSummary(
    record_count=100,
    variables=['temperature', 'salinity'],
    spatial_coverage={'min_lat': -90, 'max_lat': 90, 'min_lon': -180, 'max_lon': 180},
    temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
    depth_coverage={'min_depth': 0, 'max_depth': 2000},
    data_sources=['ARGO'],
    qc_summary={'good': 90, 'questionable': 10}
)

print("DataSummary object:")
print(test_summary)
print("\nDataSummary dict:")
print(test_summary.dict())
print("\nDataSummary JSON:")
print(test_summary.json())

# Test if it has get method
print(f"\nHas 'get' method: {hasattr(test_summary, 'get')}")
print(f"Record count via attribute: {test_summary.record_count}")

try:
    print(f"Record count via get: {test_summary.get('record_count', 0)}")
except AttributeError as e:
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    print(f"Error using get(): {e}")