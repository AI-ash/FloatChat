<<<<<<< HEAD
"""
FastAPI backend for FloatChat
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from config.settings import settings
from backend.models import QueryRequest, QueryResponse, DataExportRequest, DataSummary
from backend.database import get_db_session
from backend.services.llm_service import LLMService
from backend.services.data_service import DataService
from backend.services.mock_data_service import MockDataService
from backend.services.fast_data_service import FastDataService
from backend.services.visualization_service import VisualizationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered ARGO oceanographic data system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
data_service = DataService()
mock_data_service = MockDataService()
fast_data_service = FastDataService()
viz_service = VisualizationService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting FloatChat backend...")
    await llm_service.initialize()
    await data_service.initialize()
    await mock_data_service.initialize()
    await fast_data_service.initialize()
    await viz_service.initialize()
    logger.info("Backend services initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on shutdown"""
    logger.info("Shutting down FloatChat backend...")
    # Fast data service doesn't need cleanup
    logger.info("Backend services cleaned up")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FloatChat API is running",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/test")
async def test_data_summary():
    """Test endpoint to debug DataSummary serialization"""
    test_summary = DataSummary(
        record_count=10,
        variables=['temperature'],
        spatial_coverage={'min_lat': -90.0, 'max_lat': 90.0, 'min_lon': -180.0, 'max_lon': 180.0},
        temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
        depth_coverage={'min_depth': 0.0, 'max_depth': 2000.0},
        data_sources=['TEST'],
        qc_summary={'good': 10, 'questionable': 0, 'bad': 0}
    )
    
    return JSONResponse(content=jsonable_encoder(test_summary))

@app.post("/api/query")
async def process_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    db_session=Depends(get_db_session)
):
    """
    Process natural language query and return oceanographic data
    """
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Parse query using LLM
        parsed_query = await llm_service.parse_query(request.query)
        
        # Fetch data based on parsed parameters - use fast data service
        try:
            logger.info("Fetching realistic oceanographic data...")
            data_result = await fast_data_service.fetch_data(
                variables=parsed_query.variables,
                spatial_bounds=parsed_query.spatial_bounds,
                temporal_bounds=parsed_query.temporal_bounds,
                depth_range=parsed_query.depth_range,
                qc_flags=settings.ACCEPTED_QC_FLAGS
            )
            logger.info(f"Successfully fetched {data_result.record_count} records from fast data service")
            
        except Exception as fast_data_error:
            logger.warning(f"Fast data service failed: {fast_data_error}, trying database...")
            try:
                data_result = await data_service.fetch_data(
                    variables=parsed_query.variables,
                    spatial_bounds=parsed_query.spatial_bounds,
                    temporal_bounds=parsed_query.temporal_bounds,
                    depth_range=parsed_query.depth_range,
                    qc_flags=settings.ACCEPTED_QC_FLAGS,
                    db_session=db_session
                )
                if data_result.record_count == 0:
                    logger.info("No database data found, using mock data")
                    data_result = await mock_data_service.fetch_data(
                        variables=parsed_query.variables,
                        spatial_bounds=parsed_query.spatial_bounds,
                        temporal_bounds=parsed_query.temporal_bounds,
                        depth_range=parsed_query.depth_range,
                        qc_flags=settings.ACCEPTED_QC_FLAGS
                    )
            except Exception as db_error:
                logger.warning(f"Database service failed: {db_error}, using mock data")
                data_result = await mock_data_service.fetch_data(
                    variables=parsed_query.variables,
                    spatial_bounds=parsed_query.spatial_bounds,
                    temporal_bounds=parsed_query.temporal_bounds,
                    depth_range=parsed_query.depth_range,
                    qc_flags=settings.ACCEPTED_QC_FLAGS
                )
        
        # Generate visualizations
        visualizations = await viz_service.create_visualizations(
            data=data_result.data,
            query_type=parsed_query.query_type,
            variables=parsed_query.variables
        )
        
        # Generate natural language response
        response_text = await llm_service.generate_response(
            query=request.query,
            data_summary=data_result.summary,
            visualizations=visualizations
        )
        
        # Log query for analytics (background task)
        background_tasks.add_task(
            log_query_analytics,
            request.query,
            parsed_query,
            data_result.record_count
        )
        
        response_obj = QueryResponse(
            query=request.query,
            response=response_text,
            data_summary=data_result.summary,
            visualizations=visualizations,
            provenance=data_result.provenance,
            processing_time=data_result.processing_time
        )
        
        return JSONResponse(content=jsonable_encoder(response_obj))
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/variables")
async def get_available_variables():
    """Get list of available oceanographic variables"""
    return await data_service.get_available_variables()

@app.get("/api/data/regions")
async def get_predefined_regions():
    """Get list of predefined geographic regions"""
    return {
        "regions": [
            {"name": "Bay of Bengal", "bounds": [80.0, 5.0, 100.0, 25.0]},
            {"name": "Arabian Sea", "bounds": [60.0, 8.0, 80.0, 25.0]},
            {"name": "Indian Ocean", "bounds": [40.0, -40.0, 120.0, 30.0]},
            {"name": "Equatorial Indian Ocean", "bounds": [50.0, -10.0, 100.0, 10.0]}
        ]
    }

@app.post("/api/export")
async def export_data(request: DataExportRequest):
    """Export data in specified format"""
    try:
        export_result = await data_service.export_data(
            query_id=request.query_id,
            format=request.format,
            include_metadata=request.include_metadata
        )
        
        return {
            "download_url": export_result.download_url,
            "file_size": export_result.file_size,
            "expires_at": export_result.expires_at
        }
        
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/{region}")
async def get_regional_trends(
    region: str,
    variable: str = "temperature",
    years: int = 10
):
    """Get climate trends for a specific region"""
    try:
        trends = await data_service.get_climate_trends(
            region=region,
            variable=variable,
            years_back=years
        )
        
        return trends
        
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/floats/active")
async def get_active_floats(
    bbox: Optional[str] = None,
    limit: int = 100
):
    """Get currently active ARGO floats"""
    try:
        if bbox:
            bounds = [float(x) for x in bbox.split(",")]
        else:
            bounds = settings.DEFAULT_BBOX
            
        active_floats = await data_service.get_active_floats(
            spatial_bounds=bounds,
            limit=limit
        )
        
        return active_floats
        
    except Exception as e:
        logger.error(f"Error getting active floats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_query_analytics(query: str, parsed_query: Any, record_count: int):
    """Background task to log query analytics"""
    try:
        # Log to database or analytics service
        logger.info(f"Query analytics: {query} -> {record_count} records")
    except Exception as e:
        logger.error(f"Error logging analytics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
=======
"""
FastAPI backend for FloatChat
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from config.settings import settings
from backend.models import QueryRequest, QueryResponse, DataExportRequest, DataSummary
from backend.database import get_db_session
from backend.services.llm_service import LLMService
from backend.services.data_service import DataService
from backend.services.mock_data_service import MockDataService
from backend.services.fast_data_service import FastDataService
from backend.services.visualization_service import VisualizationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered ARGO oceanographic data system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
data_service = DataService()
mock_data_service = MockDataService()
fast_data_service = FastDataService()
viz_service = VisualizationService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting FloatChat backend...")
    await llm_service.initialize()
    await data_service.initialize()
    await mock_data_service.initialize()
    await fast_data_service.initialize()
    await viz_service.initialize()
    logger.info("Backend services initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on shutdown"""
    logger.info("Shutting down FloatChat backend...")
    # Fast data service doesn't need cleanup
    logger.info("Backend services cleaned up")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FloatChat API is running",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/test")
async def test_data_summary():
    """Test endpoint to debug DataSummary serialization"""
    test_summary = DataSummary(
        record_count=10,
        variables=['temperature'],
        spatial_coverage={'min_lat': -90.0, 'max_lat': 90.0, 'min_lon': -180.0, 'max_lon': 180.0},
        temporal_coverage={'start': datetime.now(), 'end': datetime.now()},
        depth_coverage={'min_depth': 0.0, 'max_depth': 2000.0},
        data_sources=['TEST'],
        qc_summary={'good': 10, 'questionable': 0, 'bad': 0}
    )
    
    return JSONResponse(content=jsonable_encoder(test_summary))

@app.post("/api/query")
async def process_query(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    db_session=Depends(get_db_session)
):
    """
    Process natural language query and return oceanographic data
    """
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Parse query using LLM
        parsed_query = await llm_service.parse_query(request.query)
        
        # Fetch data based on parsed parameters - use fast data service
        try:
            logger.info("Fetching realistic oceanographic data...")
            data_result = await fast_data_service.fetch_data(
                variables=parsed_query.variables,
                spatial_bounds=parsed_query.spatial_bounds,
                temporal_bounds=parsed_query.temporal_bounds,
                depth_range=parsed_query.depth_range,
                qc_flags=settings.ACCEPTED_QC_FLAGS
            )
            logger.info(f"Successfully fetched {data_result.record_count} records from fast data service")
            
        except Exception as fast_data_error:
            logger.warning(f"Fast data service failed: {fast_data_error}, trying database...")
            try:
                data_result = await data_service.fetch_data(
                    variables=parsed_query.variables,
                    spatial_bounds=parsed_query.spatial_bounds,
                    temporal_bounds=parsed_query.temporal_bounds,
                    depth_range=parsed_query.depth_range,
                    qc_flags=settings.ACCEPTED_QC_FLAGS,
                    db_session=db_session
                )
                if data_result.record_count == 0:
                    logger.info("No database data found, using mock data")
                    data_result = await mock_data_service.fetch_data(
                        variables=parsed_query.variables,
                        spatial_bounds=parsed_query.spatial_bounds,
                        temporal_bounds=parsed_query.temporal_bounds,
                        depth_range=parsed_query.depth_range,
                        qc_flags=settings.ACCEPTED_QC_FLAGS
                    )
            except Exception as db_error:
                logger.warning(f"Database service failed: {db_error}, using mock data")
                data_result = await mock_data_service.fetch_data(
                    variables=parsed_query.variables,
                    spatial_bounds=parsed_query.spatial_bounds,
                    temporal_bounds=parsed_query.temporal_bounds,
                    depth_range=parsed_query.depth_range,
                    qc_flags=settings.ACCEPTED_QC_FLAGS
                )
        
        # Generate visualizations
        visualizations = await viz_service.create_visualizations(
            data=data_result.data,
            query_type=parsed_query.query_type,
            variables=parsed_query.variables
        )
        
        # Generate natural language response
        response_text = await llm_service.generate_response(
            query=request.query,
            data_summary=data_result.summary,
            visualizations=visualizations
        )
        
        # Log query for analytics (background task)
        background_tasks.add_task(
            log_query_analytics,
            request.query,
            parsed_query,
            data_result.record_count
        )
        
        response_obj = QueryResponse(
            query=request.query,
            response=response_text,
            data_summary=data_result.summary,
            visualizations=visualizations,
            provenance=data_result.provenance,
            processing_time=data_result.processing_time
        )
        
        return JSONResponse(content=jsonable_encoder(response_obj))
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/variables")
async def get_available_variables():
    """Get list of available oceanographic variables"""
    return await data_service.get_available_variables()

@app.get("/api/data/regions")
async def get_predefined_regions():
    """Get list of predefined geographic regions"""
    return {
        "regions": [
            {"name": "Bay of Bengal", "bounds": [80.0, 5.0, 100.0, 25.0]},
            {"name": "Arabian Sea", "bounds": [60.0, 8.0, 80.0, 25.0]},
            {"name": "Indian Ocean", "bounds": [40.0, -40.0, 120.0, 30.0]},
            {"name": "Equatorial Indian Ocean", "bounds": [50.0, -10.0, 100.0, 10.0]}
        ]
    }

@app.post("/api/export")
async def export_data(request: DataExportRequest):
    """Export data in specified format"""
    try:
        export_result = await data_service.export_data(
            query_id=request.query_id,
            format=request.format,
            include_metadata=request.include_metadata
        )
        
        return {
            "download_url": export_result.download_url,
            "file_size": export_result.file_size,
            "expires_at": export_result.expires_at
        }
        
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/{region}")
async def get_regional_trends(
    region: str,
    variable: str = "temperature",
    years: int = 10
):
    """Get climate trends for a specific region"""
    try:
        trends = await data_service.get_climate_trends(
            region=region,
            variable=variable,
            years_back=years
        )
        
        return trends
        
    except Exception as e:
        logger.error(f"Error getting trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/floats/active")
async def get_active_floats(
    bbox: Optional[str] = None,
    limit: int = 100
):
    """Get currently active ARGO floats"""
    try:
        if bbox:
            bounds = [float(x) for x in bbox.split(",")]
        else:
            bounds = settings.DEFAULT_BBOX
            
        active_floats = await data_service.get_active_floats(
            spatial_bounds=bounds,
            limit=limit
        )
        
        return active_floats
        
    except Exception as e:
        logger.error(f"Error getting active floats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_query_analytics(query: str, parsed_query: Any, record_count: int):
    """Background task to log query analytics"""
    try:
        # Log to database or analytics service
        logger.info(f"Query analytics: {query} -> {record_count} records")
    except Exception as e:
        logger.error(f"Error logging analytics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
    )