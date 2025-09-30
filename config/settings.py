"""
Configuration settings for FloatChat application
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "FloatChat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Cloud Database (Supabase PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres:your_password@db.your_project.supabase.co:5432/postgres"
    # Cloud AI Services
    OPENAI_API_KEY: str = ""  # OpenAI GPT-4 API (optional backup)
    COHERE_API_KEY: str = ""  # Cohere API for embeddings
    
    # Groq API (Fast LLM inference)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    
    # Vector Database (Pinecone)
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "floatchat-knowledge"
    
    # Data Sources (Public APIs - No Registration Required)
    ARGO_API_BASE: str = "https://data-argo.ifremer.fr"
    ERDDAP_BASE: str = "https://www.ifremer.fr/erddap"
    COPERNICUS_MARINE_BASE: str = "https://marine.copernicus.eu"
    NOAA_ERDDAP_BASE: str = "https://coastwatch.pfeg.noaa.gov/erddap"
    # Redis Cloud for caching
    REDIS_URL: str = "redis://default:password@redis-cloud-url:port"
    
    # Geospatial
    DEFAULT_BBOX: List[float] = [68.0, 6.0, 97.0, 37.0]  # India region
    DEFAULT_DEPTH_RANGE: List[float] = [0, 2000]
    
    # User Roles
    USER_ROLES: Dict[str, List[str]] = {
        "student": ["basic_query", "view_maps", "export_csv"],
        "researcher": ["advanced_query", "custom_analysis", "export_netcdf", "api_access"],
        "policymaker": ["trend_dashboard", "alerts", "summary_reports"]
    }
    
    # Quality Control
    QC_FLAGS: Dict[int, str] = {
        1: "good",
        2: "probably_good", 
        3: "probably_bad",
        4: "bad",
        5: "changed",
        8: "estimated",
        9: "missing"
    }
    ACCEPTED_QC_FLAGS: List[int] = [1, 2, 5, 8]
    
    # Visualization
    MAP_TILES: str = "OpenStreetMap"
    DEFAULT_MAP_CENTER: List[float] = [20.0, 77.0]  # India center
    DEFAULT_MAP_ZOOM: int = 5
    
    # Export Formats
    SUPPORTED_EXPORT_FORMATS: List[str] = ["csv", "netcdf", "pdf", "json"]
    

    

    

    
    class Config:
        env_file = None  # Disable .env file loading
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

# Global settings instance
settings = Settings()