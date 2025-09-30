"""
Cloud database configuration and models for FloatChat (Supabase PostgreSQL)
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
import uuid
from datetime import datetime
from typing import Generator
import redis


from config.settings import settings

# Cloud Database engine (Supabase PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,
    # SSL required for cloud databases
    connect_args={"sslmode": "require"}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Redis Cloud client for caching
redis_client = None
if settings.REDIS_URL:
    try:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    except Exception as e:
        print(f"Redis connection failed: {e}")

# No file storage - everything in memory
print("✅ In-memory processing configured")

class ArgoProfile(Base):
    """ARGO float profile data table"""
    __tablename__ = "argo_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    float_id = Column(String(20), nullable=False, index=True)
    cycle_number = Column(Integer, nullable=False)
    profile_date = Column(DateTime, nullable=False, index=True)
    location = Column(Geometry('POINT'), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Measurements stored as JSON
    temperature = Column(JSON)  # {depths: [...], values: [...], qc_flags: [...]}
    salinity = Column(JSON)
    pressure = Column(JSON)
    oxygen = Column(JSON)
    
    # Metadata
    platform_type = Column(String(50))
    data_center = Column(String(10))
    data_mode = Column(String(1))  # R=real-time, D=delayed-mode, A=adjusted
    processing_date = Column(DateTime, default=datetime.utcnow)
    
    # Quality control
    position_qc = Column(Integer, default=1)
    profile_qc = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QueryLog(Base):
    """Log of user queries for analytics"""
    __tablename__ = "query_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    user_role = Column(String(20), nullable=False)
    parsed_parameters = Column(JSON)
    
    # Results
    records_returned = Column(Integer, default=0)
    processing_time = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Context
    user_location = Column(Geometry('POINT'))
    session_id = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)

class DataSource(Base):
    """Track data sources and their metadata"""
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    source_type = Column(String(20), nullable=False)  # api, file, database
    url = Column(String(500))
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_update = Column(DateTime)
    update_frequency = Column(String(20))  # daily, weekly, monthly
    
    # Metadata
    variables_available = Column(JSON)
    spatial_coverage = Column(JSON)
    temporal_coverage = Column(JSON)
    quality_info = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExportJob(Base):
    """Track data export jobs"""
    __tablename__ = "export_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), nullable=False)
    format = Column(String(10), nullable=False)
    
    # Status
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    file_path = Column(String(500))
    file_size = Column(Integer)
    download_url = Column(String(500))
    
    # Metadata
    include_metadata = Column(Boolean, default=True)
    custom_filename = Column(String(200))
    expires_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrendCache(Base):
    """Cache computed trends for performance"""
    __tablename__ = "trend_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region = Column(String(100), nullable=False)
    variable = Column(String(50), nullable=False)
    time_period = Column(String(20), nullable=False)  # e.g., "10_years"
    
    # Cached results
    trend_data = Column(JSON, nullable=False)
    computed_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Make combination unique
    __table_args__ = (
        {'schema': None},
    )

def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables in cloud database"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)

def get_cache_client():
    """Get Redis cache client"""
    return redis_client

def get_storage_client():
    """No storage client - everything in memory"""
    return None

# Initialize database on import
if __name__ == "__main__":
    create_tables()
    print("Cloud database tables created successfully!")