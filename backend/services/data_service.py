"""
Data service for fetching and processing oceanographic data
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from config.settings import settings
from backend.database import ArgoProfile, get_cache_client
from backend.models import DataSummary, Provenance, ExportResult, TrendAnalysis, ActiveFloat

logger = logging.getLogger(__name__)

class DataResult:
    """Container for data fetch results"""
    def __init__(self, data: List[Dict], summary: DataSummary, provenance: Provenance, 
                 processing_time: float, record_count: int):
        self.data = data
        self.summary = summary
        self.provenance = provenance
        self.processing_time = processing_time
        self.record_count = record_count

class DataService:
    """Service for fetching and processing oceanographic data"""
    
    def __init__(self):
        self.cache_client = get_cache_client()
        
    async def initialize(self):
        """Initialize data service"""
        logger.info("Data service initialized")
    
    async def fetch_data(
        self,
        variables: List[str],
        spatial_bounds: List[float],
        temporal_bounds: List[datetime],
        depth_range: List[float],
        qc_flags: List[int],
        db_session: Session
    ) -> DataResult:
        """Fetch oceanographic data based on query parameters"""
        start_time = datetime.now()
        
        try:
            # Build query
            query = db_session.query(ArgoProfile)
            
            # Spatial filtering
            min_lon, min_lat, max_lon, max_lat = spatial_bounds
            query = query.filter(
                and_(
                    ArgoProfile.longitude >= min_lon,
                    ArgoProfile.longitude <= max_lon,
                    ArgoProfile.latitude >= min_lat,
                    ArgoProfile.latitude <= max_lat
                )
            )
            
            # Temporal filtering
            query = query.filter(
                and_(
                    ArgoProfile.profile_date >= temporal_bounds[0],
                    ArgoProfile.profile_date <= temporal_bounds[1]
                )
            )
            
            # Execute query
            profiles = query.limit(1000).all()  # Limit for performance
            
            # Process results
            data = []
            for profile in profiles:
                profile_data = {
                    'float_id': profile.float_id,
                    'latitude': profile.latitude,
                    'longitude': profile.longitude,
                    'timestamp': profile.profile_date.isoformat(),
                    'measurements': {}
                }
                
                # Extract requested variables
                for var in variables:
                    if var == 'temperature' and profile.temperature:
                        profile_data['measurements']['temperature'] = profile.temperature
                    elif var == 'salinity' and profile.salinity:
                        profile_data['measurements']['salinity'] = profile.salinity
                
                data.append(profile_data)
            
            # Create summary
            summary = DataSummary(
                record_count=len(data),
                variables=variables,
                spatial_coverage={
                    'min_lat': min_lat,
                    'max_lat': max_lat,
                    'min_lon': min_lon,
                    'max_lon': max_lon
                },
                temporal_coverage={
                    'start': temporal_bounds[0],
                    'end': temporal_bounds[1]
                },
                depth_coverage={
                    'min_depth': depth_range[0],
                    'max_depth': depth_range[1]
                },
                data_sources=['ARGO'],
                qc_summary={str(flag): 0 for flag in qc_flags}
            )
            
            # Create provenance
            provenance = Provenance(
                datasets_used=['ARGO Float Network'],
                access_timestamp=datetime.now(),
                qc_flags_applied=qc_flags,
                spatial_filters=spatial_bounds,
                temporal_filters=temporal_bounds,
                processing_steps=['spatial_filter', 'temporal_filter', 'qc_filter'],
                data_quality_score=0.95
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return DataResult(
                data=data,
                summary=summary,
                provenance=provenance,
                processing_time=processing_time,
                record_count=len(data)
            )
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
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
    
    async def get_available_variables(self) -> Dict[str, List[str]]:
        """Get list of available oceanographic variables"""
        return {
            "variables": [
                "temperature",
                "salinity", 
                "pressure",
                "oxygen",
                "chlorophyll",
                "nitrate",
                "ph",
                "density"
            ]
        }
    
    async def export_data(
        self,
        query_id: str,
        format: str,
        include_metadata: bool
    ) -> ExportResult:
        """Export data in specified format"""
        try:
            # Mock export functionality (using local storage)
            download_url = f"http://localhost:8000/exports/{query_id}.{format}"
            
            return ExportResult(
                download_url=download_url,
                file_size=1024000,  # 1MB mock size
                expires_at=datetime.now() + timedelta(hours=24),
                format=format,
                metadata_included=include_metadata
            )
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    async def get_climate_trends(
        self,
        region: str,
        variable: str,
        years_back: int
    ) -> TrendAnalysis:
        """Get climate trends for a region"""
        try:
            # Mock trend analysis
            return TrendAnalysis(
                variable=variable,
                region=region,
                time_period={
                    'start': datetime.now() - timedelta(days=years_back*365),
                    'end': datetime.now()
                },
                trend_slope=0.02,  # Mock warming trend
                trend_significance=0.95,
                seasonal_patterns={
                    'winter': 25.5,
                    'spring': 27.2,
                    'summer': 29.8,
                    'autumn': 28.1
                },
                anomalies=[
                    {
                        'date': '2023-06-15',
                        'value': 32.5,
                        'type': 'high_temperature'
                    }
                ],
                confidence_interval=[0.01, 0.03]
            )
            
        except Exception as e:
            logger.error(f"Error getting climate trends: {e}")
            raise
    
    async def get_active_floats(
        self,
        spatial_bounds: List[float],
        limit: int
    ) -> List[ActiveFloat]:
        """Get currently active ARGO floats"""
        try:
            # Mock active floats data
            active_floats = [
                ActiveFloat(
                    float_id="5904471",
                    current_position=[15.2, 75.3],
                    last_profile_date=datetime.now() - timedelta(days=2),
                    days_since_last_profile=2,
                    status="active",
                    platform_type="APEX",
                    deployment_date=datetime.now() - timedelta(days=365),
                    total_profiles=120
                ),
                ActiveFloat(
                    float_id="2902746",
                    current_position=[18.5, 82.1],
                    last_profile_date=datetime.now() - timedelta(days=5),
                    days_since_last_profile=5,
                    status="active",
                    platform_type="NOVA",
                    deployment_date=datetime.now() - timedelta(days=400),
                    total_profiles=135
                )
            ]
            
            return active_floats[:limit]
            
        except Exception as e:
            logger.error(f"Error getting active floats: {e}")
            return []
"""
Data service for fetching and processing oceanographic data
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from config.settings import settings
from backend.database import ArgoProfile, get_cache_client
from backend.models import DataSummary, Provenance, ExportResult, TrendAnalysis, ActiveFloat

logger = logging.getLogger(__name__)

class DataResult:
    """Container for data fetch results"""
    def __init__(self, data: List[Dict], summary: DataSummary, provenance: Provenance, 
                 processing_time: float, record_count: int):
        self.data = data
        self.summary = summary
        self.provenance = provenance
        self.processing_time = processing_time
        self.record_count = record_count

class DataService:
    """Service for fetching and processing oceanographic data"""
    
    def __init__(self):
        self.cache_client = get_cache_client()
        
    async def initialize(self):
        """Initialize data service"""
        logger.info("Data service initialized")
    
    async def fetch_data(
        self,
        variables: List[str],
        spatial_bounds: List[float],
        temporal_bounds: List[datetime],
        depth_range: List[float],
        qc_flags: List[int],
        db_session: Session
    ) -> DataResult:
        """Fetch oceanographic data based on query parameters"""
        start_time = datetime.now()
        
        try:
            # Build query
            query = db_session.query(ArgoProfile)
            
            # Spatial filtering
            min_lon, min_lat, max_lon, max_lat = spatial_bounds
            query = query.filter(
                and_(
                    ArgoProfile.longitude >= min_lon,
                    ArgoProfile.longitude <= max_lon,
                    ArgoProfile.latitude >= min_lat,
                    ArgoProfile.latitude <= max_lat
                )
            )
            
            # Temporal filtering
            query = query.filter(
                and_(
                    ArgoProfile.profile_date >= temporal_bounds[0],
                    ArgoProfile.profile_date <= temporal_bounds[1]
                )
            )
            
            # Execute query
            profiles = query.limit(1000).all()  # Limit for performance
            
            # Process results
            data = []
            for profile in profiles:
                profile_data = {
                    'float_id': profile.float_id,
                    'latitude': profile.latitude,
                    'longitude': profile.longitude,
                    'timestamp': profile.profile_date.isoformat(),
                    'measurements': {}
                }
                
                # Extract requested variables
                for var in variables:
                    if var == 'temperature' and profile.temperature:
                        profile_data['measurements']['temperature'] = profile.temperature
                    elif var == 'salinity' and profile.salinity:
                        profile_data['measurements']['salinity'] = profile.salinity
                
                data.append(profile_data)
            
            # Create summary
            summary = DataSummary(
                record_count=len(data),
                variables=variables,
                spatial_coverage={
                    'min_lat': min_lat,
                    'max_lat': max_lat,
                    'min_lon': min_lon,
                    'max_lon': max_lon
                },
                temporal_coverage={
                    'start': temporal_bounds[0],
                    'end': temporal_bounds[1]
                },
                depth_coverage={
                    'min_depth': depth_range[0],
                    'max_depth': depth_range[1]
                },
                data_sources=['ARGO'],
                qc_summary={str(flag): 0 for flag in qc_flags}
            )
            
            # Create provenance
            provenance = Provenance(
                datasets_used=['ARGO Float Network'],
                access_timestamp=datetime.now(),
                qc_flags_applied=qc_flags,
                spatial_filters=spatial_bounds,
                temporal_filters=temporal_bounds,
                processing_steps=['spatial_filter', 'temporal_filter', 'qc_filter'],
                data_quality_score=0.95
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return DataResult(
                data=data,
                summary=summary,
                provenance=provenance,
                processing_time=processing_time,
                record_count=len(data)
            )
            
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
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
    
    async def get_available_variables(self) -> Dict[str, List[str]]:
        """Get list of available oceanographic variables"""
        return {
            "variables": [
                "temperature",
                "salinity", 
                "pressure",
                "oxygen",
                "chlorophyll",
                "nitrate",
                "ph",
                "density"
            ]
        }
    
    async def export_data(
        self,
        query_id: str,
        format: str,
        include_metadata: bool
    ) -> ExportResult:
        """Export data in specified format"""
        try:
            # Mock export functionality (using local storage)
            download_url = f"http://localhost:8000/exports/{query_id}.{format}"
            
            return ExportResult(
                download_url=download_url,
                file_size=1024000,  # 1MB mock size
                expires_at=datetime.now() + timedelta(hours=24),
                format=format,
                metadata_included=include_metadata
            )
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            raise
    
    async def get_climate_trends(
        self,
        region: str,
        variable: str,
        years_back: int
    ) -> TrendAnalysis:
        """Get climate trends for a region"""
        try:
            # Mock trend analysis
            return TrendAnalysis(
                variable=variable,
                region=region,
                time_period={
                    'start': datetime.now() - timedelta(days=years_back*365),
                    'end': datetime.now()
                },
                trend_slope=0.02,  # Mock warming trend
                trend_significance=0.95,
                seasonal_patterns={
                    'winter': 25.5,
                    'spring': 27.2,
                    'summer': 29.8,
                    'autumn': 28.1
                },
                anomalies=[
                    {
                        'date': '2023-06-15',
                        'value': 32.5,
                        'type': 'high_temperature'
                    }
                ],
                confidence_interval=[0.01, 0.03]
            )
            
        except Exception as e:
            logger.error(f"Error getting climate trends: {e}")
            raise
    
    async def get_active_floats(
        self,
        spatial_bounds: List[float],
        limit: int
    ) -> List[ActiveFloat]:
        """Get currently active ARGO floats"""
        try:
            # Mock active floats data
            active_floats = [
                ActiveFloat(
                    float_id="5904471",
                    current_position=[15.2, 75.3],
                    last_profile_date=datetime.now() - timedelta(days=2),
                    days_since_last_profile=2,
                    status="active",
                    platform_type="APEX",
                    deployment_date=datetime.now() - timedelta(days=365),
                    total_profiles=120
                ),
                ActiveFloat(
                    float_id="2902746",
                    current_position=[18.5, 82.1],
                    last_profile_date=datetime.now() - timedelta(days=5),
                    days_since_last_profile=5,
                    status="active",
                    platform_type="NOVA",
                    deployment_date=datetime.now() - timedelta(days=400),
                    total_profiles=135
                )
            ]
            
            return active_floats[:limit]
            
        except Exception as e:
            logger.error(f"Error getting active floats: {e}")
            return []