"""
Mock data service for testing without database
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import random

from backend.models import DataSummary, Provenance
from backend.services.data_service import DataResult

logger = logging.getLogger(__name__)

class MockDataService:
    """Mock data service that generates sample oceanographic data"""
    
    def __init__(self):
        pass
        
    async def initialize(self):
        """Initialize mock data service"""
        logger.info("Mock data service initialized")
    
    async def fetch_data(
        self,
        variables: List[str],
        spatial_bounds: List[float],
        temporal_bounds: List[datetime],
        depth_range: List[float],
        qc_flags: List[int],
        db_session=None
    ) -> DataResult:
        """Generate mock oceanographic data"""
        
        try:
            # Generate mock data
            data = []
            num_records = random.randint(10, 50)
            
            for i in range(num_records):
                # Random location within bounds
                lat = random.uniform(spatial_bounds[1], spatial_bounds[3])
                lon = random.uniform(spatial_bounds[0], spatial_bounds[2])
                
                # Random timestamp within bounds
                time_diff = temporal_bounds[1] - temporal_bounds[0]
                random_time = temporal_bounds[0] + timedelta(
                    seconds=random.randint(0, int(time_diff.total_seconds()))
                )
                
                # Generate measurements for each variable
                measurements = {}
                for var in variables:
                    if var == 'temperature':
                        value = random.uniform(0, 30)  # Celsius
                    elif var == 'salinity':
                        value = random.uniform(30, 40)  # PSU
                    elif var == 'pressure':
                        value = random.uniform(depth_range[0], depth_range[1])
                    else:
                        value = random.uniform(0, 100)
                    
                    measurements[var] = {
                        'values': [value],
                        'depths': [random.uniform(depth_range[0], depth_range[1])],
                        'qc_flags': [1]  # Good quality
                    }
                
                profile_data = {
                    'float_id': f'MOCK{2900000 + i}',
                    'cycle_number': random.randint(1, 100),
                    'latitude': lat,
                    'longitude': lon,
                    'timestamp': random_time,
                    'measurements': measurements
                }
                
                data.append(profile_data)
            
            # Create summary
            summary = DataSummary(
                record_count=len(data),
                variables=variables,
                spatial_coverage={
                    'min_lat': spatial_bounds[1],
                    'max_lat': spatial_bounds[3],
                    'min_lon': spatial_bounds[0],
                    'max_lon': spatial_bounds[2]
                },
                temporal_coverage={
                    'start': temporal_bounds[0],
                    'end': temporal_bounds[1]
                },
                depth_coverage={
                    'min_depth': depth_range[0],
                    'max_depth': depth_range[1]
                },
                data_sources=['MOCK_ARGO'],
                qc_summary={'good': len(data), 'questionable': 0, 'bad': 0}
            )
            
            # Create provenance
            provenance = Provenance(
                datasets_used=['Mock ARGO Dataset'],
                access_timestamp=datetime.now(),
                qc_flags_applied=qc_flags,
                spatial_filters=spatial_bounds,
                temporal_filters=temporal_bounds,
                processing_steps=['Mock data generation', 'Quality control applied'],
                data_quality_score=0.95
            )
            
            return DataResult(
                data=data,
                summary=summary,
                provenance=provenance,
                processing_time=0.1,
                record_count=len(data)
            )
            
        except Exception as e:
            logger.error(f"Error generating mock data: {e}")
            # Return empty result
            return DataResult(
                data=[],
                summary=DataSummary(
                    record_count=0,
                    variables=variables,
                    spatial_coverage={
                        "min_lat": 0.0, "max_lat": 0.0, 
                        "min_lon": 0.0, "max_lon": 0.0
                    },
                    temporal_coverage={
                        "start": datetime.now(), 
                        "end": datetime.now()
                    },
                    depth_coverage={
                        "min_depth": 0.0, 
                        "max_depth": 0.0
                    },
                    data_sources=[],
                    qc_summary={"good": 0, "questionable": 0, "bad": 0}
                ),
                provenance=Provenance(
                    datasets_used=[],
                    access_timestamp=datetime.now(),
                    qc_flags_applied=[],
                    spatial_filters=[],
                    temporal_filters=[],
                    processing_steps=[],
                    data_quality_score=0.0
                ),
                processing_time=0.0,
                record_count=0
            )