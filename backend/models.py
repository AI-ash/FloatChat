<<<<<<< HEAD
"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RESEARCHER = "researcher"
    POLICYMAKER = "policymaker"

class QueryType(str, Enum):
    PROFILE = "profile"
    TIMESERIES = "timeseries"
    SPATIAL = "spatial"
    TRAJECTORY = "trajectory"
    TREND = "trend"
    COMPARISON = "comparison"

class ExportFormat(str, Enum):
    CSV = "csv"
    NETCDF = "netcdf"
    PDF = "pdf"
    JSON = "json"

class QueryRequest(BaseModel):
    """Request model for natural language queries"""
    query: str = Field(..., description="Natural language query")
    user_role: UserRole = Field(UserRole.STUDENT, description="User role for permissions")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    user_location: Optional[List[float]] = Field(None, description="User's lat/lon for location-based queries")

class ParsedQuery(BaseModel):
    """Parsed query parameters extracted by LLM"""
    variables: List[str] = Field(..., description="Oceanographic variables requested")
    spatial_bounds: List[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]")
    temporal_bounds: List[datetime] = Field(..., description="[start_time, end_time]")
    depth_range: List[float] = Field(..., description="[min_depth, max_depth] in meters")
    query_type: QueryType = Field(..., description="Type of query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")

class DataSummary(BaseModel):
    """Summary of fetched data"""
    record_count: int
    variables: List[str]
    spatial_coverage: Dict[str, float]
    temporal_coverage: Dict[str, datetime]
    depth_coverage: Dict[str, float]
    data_sources: List[str]
    qc_summary: Dict[str, int]

class Visualization(BaseModel):
    """Visualization metadata"""
    type: str = Field(..., description="Type of visualization (map, plot, 3d)")
    title: str
    data_url: Optional[str] = Field(None, description="URL to visualization data")
    config: Dict[str, Any] = Field(..., description="Visualization configuration")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")

class Provenance(BaseModel):
    """Data provenance information"""
    datasets_used: List[str]
    access_timestamp: datetime
    qc_flags_applied: List[int]
    spatial_filters: List[float]
    temporal_filters: List[datetime]
    processing_steps: List[str]
    data_quality_score: float = Field(..., ge=0.0, le=1.0)

class QueryResponse(BaseModel):
    """Response model for processed queries"""
    query: str
    response: str = Field(..., description="Natural language response")
    data_summary: DataSummary
    visualizations: List[Visualization]
    provenance: Provenance
    processing_time: float = Field(..., description="Processing time in seconds")
    suggested_followups: Optional[List[str]] = Field(None, description="Suggested follow-up queries")

class DataExportRequest(BaseModel):
    """Request model for data export"""
    query_id: str = Field(..., description="ID of the query to export")
    format: ExportFormat = Field(..., description="Export format")
    include_metadata: bool = Field(True, description="Include metadata in export")
    custom_filename: Optional[str] = Field(None, description="Custom filename")

class ExportResult(BaseModel):
    """Result of data export operation"""
    download_url: str
    file_size: int
    expires_at: datetime
    format: ExportFormat
    metadata_included: bool

class FloatProfile(BaseModel):
    """ARGO float profile data"""
    float_id: str
    cycle_number: int
    latitude: float
    longitude: float
    timestamp: datetime
    measurements: Dict[str, List[float]]  # variable -> [values by depth]
    depths: List[float]
    qc_flags: Dict[str, List[int]]
    platform_type: str
    data_center: str

class TrendAnalysis(BaseModel):
    """Climate trend analysis result"""
    variable: str
    region: str
    time_period: Dict[str, datetime]
    trend_slope: float
    trend_significance: float
    seasonal_patterns: Dict[str, float]
    anomalies: List[Dict[str, Any]]
    confidence_interval: List[float]

class ActiveFloat(BaseModel):
    """Active ARGO float information"""
    float_id: str
    current_position: List[float]  # [lat, lon]
    last_profile_date: datetime
    days_since_last_profile: int
    status: str
    platform_type: str
    deployment_date: datetime
    total_profiles: int

class RegionInfo(BaseModel):
    """Geographic region information"""
    name: str
    bounds: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    description: Optional[str] = None
    typical_variables: List[str]
    seasonal_patterns: Optional[Dict[str, str]] = None

class QualityControlInfo(BaseModel):
    """Quality control information"""
    flag_value: int
    flag_meaning: str
    description: str
=======
"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RESEARCHER = "researcher"
    POLICYMAKER = "policymaker"

class QueryType(str, Enum):
    PROFILE = "profile"
    TIMESERIES = "timeseries"
    SPATIAL = "spatial"
    TRAJECTORY = "trajectory"
    TREND = "trend"
    COMPARISON = "comparison"

class ExportFormat(str, Enum):
    CSV = "csv"
    NETCDF = "netcdf"
    PDF = "pdf"
    JSON = "json"

class QueryRequest(BaseModel):
    """Request model for natural language queries"""
    query: str = Field(..., description="Natural language query")
    user_role: UserRole = Field(UserRole.STUDENT, description="User role for permissions")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    user_location: Optional[List[float]] = Field(None, description="User's lat/lon for location-based queries")

class ParsedQuery(BaseModel):
    """Parsed query parameters extracted by LLM"""
    variables: List[str] = Field(..., description="Oceanographic variables requested")
    spatial_bounds: List[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]")
    temporal_bounds: List[datetime] = Field(..., description="[start_time, end_time]")
    depth_range: List[float] = Field(..., description="[min_depth, max_depth] in meters")
    query_type: QueryType = Field(..., description="Type of query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Additional filters")

class DataSummary(BaseModel):
    """Summary of fetched data"""
    record_count: int
    variables: List[str]
    spatial_coverage: Dict[str, float]
    temporal_coverage: Dict[str, datetime]
    depth_coverage: Dict[str, float]
    data_sources: List[str]
    qc_summary: Dict[str, int]

class Visualization(BaseModel):
    """Visualization metadata"""
    type: str = Field(..., description="Type of visualization (map, plot, 3d)")
    title: str
    data_url: Optional[str] = Field(None, description="URL to visualization data")
    config: Dict[str, Any] = Field(..., description="Visualization configuration")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")

class Provenance(BaseModel):
    """Data provenance information"""
    datasets_used: List[str]
    access_timestamp: datetime
    qc_flags_applied: List[int]
    spatial_filters: List[float]
    temporal_filters: List[datetime]
    processing_steps: List[str]
    data_quality_score: float = Field(..., ge=0.0, le=1.0)

class QueryResponse(BaseModel):
    """Response model for processed queries"""
    query: str
    response: str = Field(..., description="Natural language response")
    data_summary: DataSummary
    visualizations: List[Visualization]
    provenance: Provenance
    processing_time: float = Field(..., description="Processing time in seconds")
    suggested_followups: Optional[List[str]] = Field(None, description="Suggested follow-up queries")

class DataExportRequest(BaseModel):
    """Request model for data export"""
    query_id: str = Field(..., description="ID of the query to export")
    format: ExportFormat = Field(..., description="Export format")
    include_metadata: bool = Field(True, description="Include metadata in export")
    custom_filename: Optional[str] = Field(None, description="Custom filename")

class ExportResult(BaseModel):
    """Result of data export operation"""
    download_url: str
    file_size: int
    expires_at: datetime
    format: ExportFormat
    metadata_included: bool

class FloatProfile(BaseModel):
    """ARGO float profile data"""
    float_id: str
    cycle_number: int
    latitude: float
    longitude: float
    timestamp: datetime
    measurements: Dict[str, List[float]]  # variable -> [values by depth]
    depths: List[float]
    qc_flags: Dict[str, List[int]]
    platform_type: str
    data_center: str

class TrendAnalysis(BaseModel):
    """Climate trend analysis result"""
    variable: str
    region: str
    time_period: Dict[str, datetime]
    trend_slope: float
    trend_significance: float
    seasonal_patterns: Dict[str, float]
    anomalies: List[Dict[str, Any]]
    confidence_interval: List[float]

class ActiveFloat(BaseModel):
    """Active ARGO float information"""
    float_id: str
    current_position: List[float]  # [lat, lon]
    last_profile_date: datetime
    days_since_last_profile: int
    status: str
    platform_type: str
    deployment_date: datetime
    total_profiles: int

class RegionInfo(BaseModel):
    """Geographic region information"""
    name: str
    bounds: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    description: Optional[str] = None
    typical_variables: List[str]
    seasonal_patterns: Optional[Dict[str, str]] = None

class QualityControlInfo(BaseModel):
    """Quality control information"""
    flag_value: int
    flag_meaning: str
    description: str
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    recommended_use: bool