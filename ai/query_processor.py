"""
Cloud-based query processing with RAG using Pinecone
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import re

# Cloud services
import pinecone
import cohere
from openai import AsyncOpenAI

from config.settings import settings
from backend.models import ParsedQuery, QueryType

logger = logging.getLogger(__name__)

class CloudOceanographicRetriever:
    """Cloud-based retriever using Pinecone vector database"""
    
    def __init__(self):
        self.pinecone_index = None
        self.cohere_client = None
        self._initialize_cloud_services()
    
    def _initialize_cloud_services(self):
        """Initialize cloud vector database and embedding services"""
        try:
            # Initialize Pinecone
            if settings.PINECONE_API_KEY:
                pinecone.init(
                    api_key=settings.PINECONE_API_KEY,
                    environment=settings.PINECONE_ENVIRONMENT
                )
                
                # Create or connect to index
                if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                    pinecone.create_index(
                        name=settings.PINECONE_INDEX_NAME,
                        dimension=1024,  # Cohere embedding dimension
                        metric="cosine"
                    )
                
                self.pinecone_index = pinecone.Index(settings.PINECONE_INDEX_NAME)
            
            # Initialize Cohere for embeddings
            if settings.COHERE_API_KEY:
                self.cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)
            
            # Populate knowledge base if empty
            self._populate_knowledge_base()
            
            logger.info("Cloud retriever services initialized")
            
        except Exception as e:
            logger.error(f"Error initializing cloud services: {e}")
    
    def _populate_knowledge_base(self):
        """Populate Pinecone with oceanographic knowledge"""
        try:
            if not self.pinecone_index or not self.cohere_client:
                return
            
            # Check if index is already populated
            stats = self.pinecone_index.describe_index_stats()
            if stats['total_vector_count'] > 0:
                return  # Already populated
            
            # Oceanographic knowledge documents
            documents = [
                {
                    "text": "ARGO floats are autonomous profiling floats that drift with ocean currents and dive to depths of 2000m every 10 days to measure temperature, salinity, and pressure.",
                    "metadata": {"source": "argo_basics", "type": "definition"}
                },
                {
                    "text": "Temperature in the ocean varies with depth, latitude, and season. Surface temperatures are typically 25-30°C in tropical regions and decrease with depth.",
                    "metadata": {"source": "temperature_patterns", "type": "oceanography"}
                },
                {
                    "text": "Salinity is measured in practical salinity units (PSU). Ocean salinity typically ranges from 32-37 PSU, with higher values in evaporation-dominated regions.",
                    "metadata": {"source": "salinity_basics", "type": "oceanography"}
                },
                {
                    "text": "The Bay of Bengal is a large bay in the northeastern part of the Indian Ocean, bounded by India, Bangladesh, Myanmar, and Sri Lanka. It's known for low salinity due to river discharge.",
                    "metadata": {"source": "bay_of_bengal", "type": "geography"}
                },
                {
                    "text": "The Arabian Sea is bounded by India, Pakistan, Iran, Oman, Yemen, and Somalia. It has higher salinity than the Bay of Bengal due to high evaporation rates.",
                    "metadata": {"source": "arabian_sea", "type": "geography"}
                },
                {
                    "text": "Quality control flags in ARGO data: 1=good, 2=probably good, 3=probably bad, 4=bad, 5=changed, 8=estimated, 9=missing. Only flags 1, 2, 5, and 8 should be used for analysis.",
                    "metadata": {"source": "qc_flags", "type": "data_quality"}
                },
                {
                    "text": "El Niño events cause warming of sea surface temperatures in the Pacific, which can affect monsoon patterns and ocean circulation in the Indian Ocean.",
                    "metadata": {"source": "el_nino", "type": "climate"}
                },
                {
                    "text": "Ocean acidification is the ongoing decrease in pH of Earth's oceans, caused by absorption of CO2 from the atmosphere. It affects marine ecosystems and coral reefs.",
                    "metadata": {"source": "acidification", "type": "climate"}
                }
            ]
            
            # Generate embeddings and store in Pinecone
            texts = [doc["text"] for doc in documents]
            embeddings = self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            ).embeddings
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                vectors.append({
                    "id": f"doc_{i}",
                    "values": embedding,
                    "metadata": {
                        "text": doc["text"],
                        **doc["metadata"]
                    }
                })
            
            # Upload to Pinecone
            self.pinecone_index.upsert(vectors=vectors)
            logger.info("Knowledge base populated in Pinecone")
            
        except Exception as e:
            logger.error(f"Error populating knowledge base: {e}")
    
    async def get_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query using Pinecone"""
        try:
            if not self.pinecone_index or not self.cohere_client:
                return []
            
            # Generate query embedding
            query_embedding = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            ).embeddings[0]
            
            # Search in Pinecone
            results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results['matches']:
                documents.append({
                    "text": match['metadata']['text'],
                    "score": match['score'],
                    "metadata": match['metadata']
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []

class QueryProcessor:
    """Cloud-based query processor with RAG capabilities"""
    
    def __init__(self):
        self.retriever = CloudOceanographicRetriever()
        
    async def _search_knowledge(self, query: str) -> str:
        """Search the cloud oceanographic knowledge base"""
        try:
            docs = await self.retriever.get_relevant_documents(query)
            if docs:
                context = "\n".join([doc["text"] for doc in docs])
                return f"Relevant information:\n{context}"
            return "No relevant information found."
        except Exception as e:
            return f"Error searching knowledge base: {e}"
    
    def _parse_location(self, location_text: str) -> str:
        """Parse location names into coordinates"""
        try:
            location_map = {
                "bay of bengal": [80.0, 5.0, 100.0, 25.0],
                "arabian sea": [60.0, 8.0, 80.0, 25.0],
                "indian ocean": [40.0, -40.0, 120.0, 30.0],
                "equatorial indian ocean": [50.0, -10.0, 100.0, 10.0],
                "india": [68.0, 6.0, 97.0, 37.0],
                "mumbai": [72.8, 19.0, 72.9, 19.1],
                "chennai": [80.2, 13.0, 80.3, 13.1],
                "kochi": [76.2, 9.9, 76.3, 10.0]
            }
            
            location_lower = location_text.lower()
            for name, coords in location_map.items():
                if name in location_lower:
                    return f"Coordinates for {name}: {coords} (min_lon, min_lat, max_lon, max_lat)"
            
            return f"Location '{location_text}' not found in database. Using default Indian Ocean region."
            
        except Exception as e:
            return f"Error parsing location: {e}"
    
    def _parse_time_range(self, time_text: str) -> str:
        """Parse relative time expressions"""
        try:
            now = datetime.now()
            time_lower = time_text.lower()
            
            # Extract numbers
            numbers = re.findall(r'\d+', time_text)
            
            if 'last' in time_lower and 'year' in time_lower:
                years = int(numbers[0]) if numbers else 1
                start_date = now - timedelta(days=years * 365)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            elif 'last' in time_lower and 'month' in time_lower:
                months = int(numbers[0]) if numbers else 1
                start_date = now - timedelta(days=months * 30)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            elif 'recent' in time_lower or 'latest' in time_lower:
                start_date = now - timedelta(days=30)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            return f"Could not parse time range from '{time_text}'. Using last year as default."
            
        except Exception as e:
            return f"Error parsing time range: {e}"
    
    def _validate_variables(self, variables_text: str) -> str:
        """Validate and suggest oceanographic variables"""
        try:
            available_vars = {
                'temperature': ['temp', 'temperature', 'sst', 'sea surface temperature'],
                'salinity': ['sal', 'salinity', 'psal', 'practical salinity'],
                'pressure': ['pres', 'pressure', 'depth'],
                'oxygen': ['oxy', 'oxygen', 'dissolved oxygen', 'do'],
                'chlorophyll': ['chl', 'chlorophyll', 'chla'],
                'nitrate': ['no3', 'nitrate', 'nitrogen'],
                'ph': ['ph', 'acidity', 'acid'],
                'density': ['density', 'sigma', 'potential density']
            }
            
            variables_lower = variables_text.lower()
            matched_vars = []
            
            for standard_var, aliases in available_vars.items():
                for alias in aliases:
                    if alias in variables_lower:
                        matched_vars.append(standard_var)
                        break
            
            if matched_vars:
                return f"Matched variables: {matched_vars}"
            else:
                return f"No variables matched from '{variables_text}'. Available: {list(available_vars.keys())}"
                
        except Exception as e:
            return f"Error validating variables: {e}"
    
    async def process_advanced_query(self, query: str, context: Dict[str, Any] = None) -> ParsedQuery:
        """Process query using advanced NLP and RAG"""
        try:
            logger.info(f"Processing advanced query: {query}")
            
            # Get relevant context from cloud knowledge base
            relevant_docs = await self.retriever.get_relevant_documents(query)
            context_info = "\n".join([doc["text"] for doc in relevant_docs])
            
            # Use tools to extract information
            location_info = self._parse_location(query)
            time_info = self._parse_time_range(query)
            variable_info = self._validate_variables(query)
            
            # Combine information to create structured query
            parsed_query = self._create_structured_query(
                query, location_info, time_info, variable_info, context_info
            )
            
            return parsed_query
            
        except Exception as e:
            logger.error(f"Error in advanced query processing: {e}")
            return self._get_fallback_query(query)
    
    def _create_structured_query(
        self, 
        original_query: str,
        location_info: str,
        time_info: str, 
        variable_info: str,
        context_info: str
    ) -> ParsedQuery:
        """Create structured query from extracted information"""
        try:
            # Extract coordinates from location_info
            coord_match = re.search(r'\[([\d\.\-\,\s]+)\]', location_info)
            if coord_match:
                coords = [float(x.strip()) for x in coord_match.group(1).split(',')]
                spatial_bounds = coords
            else:
                spatial_bounds = settings.DEFAULT_BBOX
            
            # Extract dates from time_info
            date_matches = re.findall(r'\d{4}-\d{2}-\d{2}T[\d\:\-\.]+', time_info)
            if len(date_matches) >= 2:
                temporal_bounds = [
                    datetime.fromisoformat(date_matches[0].split('T')[0]),
                    datetime.fromisoformat(date_matches[1].split('T')[0])
                ]
            else:
                temporal_bounds = [
                    datetime.now() - timedelta(days=365),
                    datetime.now()
                ]
            
            # Extract variables from variable_info
            var_match = re.search(r'Matched variables: \[(.*?)\]', variable_info)
            if var_match:
                variables = [v.strip().strip("'\"") for v in var_match.group(1).split(',')]
            else:
                variables = ['temperature']  # Default
            
            # Determine query type
            query_type = self._determine_query_type(original_query)
            
            return ParsedQuery(
                variables=variables,
                spatial_bounds=spatial_bounds,
                temporal_bounds=temporal_bounds,
                depth_range=settings.DEFAULT_DEPTH_RANGE,
                query_type=query_type,
                filters={}
            )
            
        except Exception as e:
            logger.error(f"Error creating structured query: {e}")
            return self._get_fallback_query(original_query)
    
    def _determine_query_type(self, query: str) -> QueryType:
        """Determine the type of query based on content"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['trend', 'change', 'over time', 'years']):
            return QueryType.TIMESERIES
        elif any(word in query_lower for word in ['profile', 'depth', 'vertical']):
            return QueryType.PROFILE
        elif any(word in query_lower for word in ['trajectory', 'path', 'movement']):
            return QueryType.TRAJECTORY
        elif any(word in query_lower for word in ['compare', 'difference', 'vs']):
            return QueryType.COMPARISON
        elif any(word in query_lower for word in ['map', 'spatial', 'region', 'area']):
            return QueryType.SPATIAL
        else:
            return QueryType.SPATIAL  # Default
    
    def _get_fallback_query(self, original_query: str) -> ParsedQuery:
        """Get fallback query parameters"""
        return ParsedQuery(
            variables=['temperature'],
            spatial_bounds=settings.DEFAULT_BBOX,
            temporal_bounds=[
                datetime.now() - timedelta(days=365),
                datetime.now()
            ],
            depth_range=settings.DEFAULT_DEPTH_RANGE,
            query_type=QueryType.SPATIAL,
            filters={}
        )

# Global cloud query processor instance
query_processor = QueryProcessor()
"""
Cloud-based query processing with RAG using Pinecone
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import re

# Cloud services
import pinecone
import cohere
from openai import AsyncOpenAI

from config.settings import settings
from backend.models import ParsedQuery, QueryType

logger = logging.getLogger(__name__)

class CloudOceanographicRetriever:
    """Cloud-based retriever using Pinecone vector database"""
    
    def __init__(self):
        self.pinecone_index = None
        self.cohere_client = None
        self._initialize_cloud_services()
    
    def _initialize_cloud_services(self):
        """Initialize cloud vector database and embedding services"""
        try:
            # Initialize Pinecone
            if settings.PINECONE_API_KEY:
                pinecone.init(
                    api_key=settings.PINECONE_API_KEY,
                    environment=settings.PINECONE_ENVIRONMENT
                )
                
                # Create or connect to index
                if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                    pinecone.create_index(
                        name=settings.PINECONE_INDEX_NAME,
                        dimension=1024,  # Cohere embedding dimension
                        metric="cosine"
                    )
                
                self.pinecone_index = pinecone.Index(settings.PINECONE_INDEX_NAME)
            
            # Initialize Cohere for embeddings
            if settings.COHERE_API_KEY:
                self.cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)
            
            # Populate knowledge base if empty
            self._populate_knowledge_base()
            
            logger.info("Cloud retriever services initialized")
            
        except Exception as e:
            logger.error(f"Error initializing cloud services: {e}")
    
    def _populate_knowledge_base(self):
        """Populate Pinecone with oceanographic knowledge"""
        try:
            if not self.pinecone_index or not self.cohere_client:
                return
            
            # Check if index is already populated
            stats = self.pinecone_index.describe_index_stats()
            if stats['total_vector_count'] > 0:
                return  # Already populated
            
            # Oceanographic knowledge documents
            documents = [
                {
                    "text": "ARGO floats are autonomous profiling floats that drift with ocean currents and dive to depths of 2000m every 10 days to measure temperature, salinity, and pressure.",
                    "metadata": {"source": "argo_basics", "type": "definition"}
                },
                {
                    "text": "Temperature in the ocean varies with depth, latitude, and season. Surface temperatures are typically 25-30°C in tropical regions and decrease with depth.",
                    "metadata": {"source": "temperature_patterns", "type": "oceanography"}
                },
                {
                    "text": "Salinity is measured in practical salinity units (PSU). Ocean salinity typically ranges from 32-37 PSU, with higher values in evaporation-dominated regions.",
                    "metadata": {"source": "salinity_basics", "type": "oceanography"}
                },
                {
                    "text": "The Bay of Bengal is a large bay in the northeastern part of the Indian Ocean, bounded by India, Bangladesh, Myanmar, and Sri Lanka. It's known for low salinity due to river discharge.",
                    "metadata": {"source": "bay_of_bengal", "type": "geography"}
                },
                {
                    "text": "The Arabian Sea is bounded by India, Pakistan, Iran, Oman, Yemen, and Somalia. It has higher salinity than the Bay of Bengal due to high evaporation rates.",
                    "metadata": {"source": "arabian_sea", "type": "geography"}
                },
                {
                    "text": "Quality control flags in ARGO data: 1=good, 2=probably good, 3=probably bad, 4=bad, 5=changed, 8=estimated, 9=missing. Only flags 1, 2, 5, and 8 should be used for analysis.",
                    "metadata": {"source": "qc_flags", "type": "data_quality"}
                },
                {
                    "text": "El Niño events cause warming of sea surface temperatures in the Pacific, which can affect monsoon patterns and ocean circulation in the Indian Ocean.",
                    "metadata": {"source": "el_nino", "type": "climate"}
                },
                {
                    "text": "Ocean acidification is the ongoing decrease in pH of Earth's oceans, caused by absorption of CO2 from the atmosphere. It affects marine ecosystems and coral reefs.",
                    "metadata": {"source": "acidification", "type": "climate"}
                }
            ]
            
            # Generate embeddings and store in Pinecone
            texts = [doc["text"] for doc in documents]
            embeddings = self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            ).embeddings
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                vectors.append({
                    "id": f"doc_{i}",
                    "values": embedding,
                    "metadata": {
                        "text": doc["text"],
                        **doc["metadata"]
                    }
                })
            
            # Upload to Pinecone
            self.pinecone_index.upsert(vectors=vectors)
            logger.info("Knowledge base populated in Pinecone")
            
        except Exception as e:
            logger.error(f"Error populating knowledge base: {e}")
    
    async def get_relevant_documents(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query using Pinecone"""
        try:
            if not self.pinecone_index or not self.cohere_client:
                return []
            
            # Generate query embedding
            query_embedding = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            ).embeddings[0]
            
            # Search in Pinecone
            results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True
            )
            
            # Format results
            documents = []
            for match in results['matches']:
                documents.append({
                    "text": match['metadata']['text'],
                    "score": match['score'],
                    "metadata": match['metadata']
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []

class QueryProcessor:
    """Cloud-based query processor with RAG capabilities"""
    
    def __init__(self):
        self.retriever = CloudOceanographicRetriever()
        
    async def _search_knowledge(self, query: str) -> str:
        """Search the cloud oceanographic knowledge base"""
        try:
            docs = await self.retriever.get_relevant_documents(query)
            if docs:
                context = "\n".join([doc["text"] for doc in docs])
                return f"Relevant information:\n{context}"
            return "No relevant information found."
        except Exception as e:
            return f"Error searching knowledge base: {e}"
    
    def _parse_location(self, location_text: str) -> str:
        """Parse location names into coordinates"""
        try:
            location_map = {
                "bay of bengal": [80.0, 5.0, 100.0, 25.0],
                "arabian sea": [60.0, 8.0, 80.0, 25.0],
                "indian ocean": [40.0, -40.0, 120.0, 30.0],
                "equatorial indian ocean": [50.0, -10.0, 100.0, 10.0],
                "india": [68.0, 6.0, 97.0, 37.0],
                "mumbai": [72.8, 19.0, 72.9, 19.1],
                "chennai": [80.2, 13.0, 80.3, 13.1],
                "kochi": [76.2, 9.9, 76.3, 10.0]
            }
            
            location_lower = location_text.lower()
            for name, coords in location_map.items():
                if name in location_lower:
                    return f"Coordinates for {name}: {coords} (min_lon, min_lat, max_lon, max_lat)"
            
            return f"Location '{location_text}' not found in database. Using default Indian Ocean region."
            
        except Exception as e:
            return f"Error parsing location: {e}"
    
    def _parse_time_range(self, time_text: str) -> str:
        """Parse relative time expressions"""
        try:
            now = datetime.now()
            time_lower = time_text.lower()
            
            # Extract numbers
            numbers = re.findall(r'\d+', time_text)
            
            if 'last' in time_lower and 'year' in time_lower:
                years = int(numbers[0]) if numbers else 1
                start_date = now - timedelta(days=years * 365)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            elif 'last' in time_lower and 'month' in time_lower:
                months = int(numbers[0]) if numbers else 1
                start_date = now - timedelta(days=months * 30)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            elif 'recent' in time_lower or 'latest' in time_lower:
                start_date = now - timedelta(days=30)
                return f"Time range: {start_date.isoformat()} to {now.isoformat()}"
            
            return f"Could not parse time range from '{time_text}'. Using last year as default."
            
        except Exception as e:
            return f"Error parsing time range: {e}"
    
    def _validate_variables(self, variables_text: str) -> str:
        """Validate and suggest oceanographic variables"""
        try:
            available_vars = {
                'temperature': ['temp', 'temperature', 'sst', 'sea surface temperature'],
                'salinity': ['sal', 'salinity', 'psal', 'practical salinity'],
                'pressure': ['pres', 'pressure', 'depth'],
                'oxygen': ['oxy', 'oxygen', 'dissolved oxygen', 'do'],
                'chlorophyll': ['chl', 'chlorophyll', 'chla'],
                'nitrate': ['no3', 'nitrate', 'nitrogen'],
                'ph': ['ph', 'acidity', 'acid'],
                'density': ['density', 'sigma', 'potential density']
            }
            
            variables_lower = variables_text.lower()
            matched_vars = []
            
            for standard_var, aliases in available_vars.items():
                for alias in aliases:
                    if alias in variables_lower:
                        matched_vars.append(standard_var)
                        break
            
            if matched_vars:
                return f"Matched variables: {matched_vars}"
            else:
                return f"No variables matched from '{variables_text}'. Available: {list(available_vars.keys())}"
                
        except Exception as e:
            return f"Error validating variables: {e}"
    
    async def process_advanced_query(self, query: str, context: Dict[str, Any] = None) -> ParsedQuery:
        """Process query using advanced NLP and RAG"""
        try:
            logger.info(f"Processing advanced query: {query}")
            
            # Get relevant context from cloud knowledge base
            relevant_docs = await self.retriever.get_relevant_documents(query)
            context_info = "\n".join([doc["text"] for doc in relevant_docs])
            
            # Use tools to extract information
            location_info = self._parse_location(query)
            time_info = self._parse_time_range(query)
            variable_info = self._validate_variables(query)
            
            # Combine information to create structured query
            parsed_query = self._create_structured_query(
                query, location_info, time_info, variable_info, context_info
            )
            
            return parsed_query
            
        except Exception as e:
            logger.error(f"Error in advanced query processing: {e}")
            return self._get_fallback_query(query)
    
    def _create_structured_query(
        self, 
        original_query: str,
        location_info: str,
        time_info: str, 
        variable_info: str,
        context_info: str
    ) -> ParsedQuery:
        """Create structured query from extracted information"""
        try:
            # Extract coordinates from location_info
            coord_match = re.search(r'\[([\d\.\-\,\s]+)\]', location_info)
            if coord_match:
                coords = [float(x.strip()) for x in coord_match.group(1).split(',')]
                spatial_bounds = coords
            else:
                spatial_bounds = settings.DEFAULT_BBOX
            
            # Extract dates from time_info
            date_matches = re.findall(r'\d{4}-\d{2}-\d{2}T[\d\:\-\.]+', time_info)
            if len(date_matches) >= 2:
                temporal_bounds = [
                    datetime.fromisoformat(date_matches[0].split('T')[0]),
                    datetime.fromisoformat(date_matches[1].split('T')[0])
                ]
            else:
                temporal_bounds = [
                    datetime.now() - timedelta(days=365),
                    datetime.now()
                ]
            
            # Extract variables from variable_info
            var_match = re.search(r'Matched variables: \[(.*?)\]', variable_info)
            if var_match:
                variables = [v.strip().strip("'\"") for v in var_match.group(1).split(',')]
            else:
                variables = ['temperature']  # Default
            
            # Determine query type
            query_type = self._determine_query_type(original_query)
            
            return ParsedQuery(
                variables=variables,
                spatial_bounds=spatial_bounds,
                temporal_bounds=temporal_bounds,
                depth_range=settings.DEFAULT_DEPTH_RANGE,
                query_type=query_type,
                filters={}
            )
            
        except Exception as e:
            logger.error(f"Error creating structured query: {e}")
            return self._get_fallback_query(original_query)
    
    def _determine_query_type(self, query: str) -> QueryType:
        """Determine the type of query based on content"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['trend', 'change', 'over time', 'years']):
            return QueryType.TIMESERIES
        elif any(word in query_lower for word in ['profile', 'depth', 'vertical']):
            return QueryType.PROFILE
        elif any(word in query_lower for word in ['trajectory', 'path', 'movement']):
            return QueryType.TRAJECTORY
        elif any(word in query_lower for word in ['compare', 'difference', 'vs']):
            return QueryType.COMPARISON
        elif any(word in query_lower for word in ['map', 'spatial', 'region', 'area']):
            return QueryType.SPATIAL
        else:
            return QueryType.SPATIAL  # Default
    
    def _get_fallback_query(self, original_query: str) -> ParsedQuery:
        """Get fallback query parameters"""
        return ParsedQuery(
            variables=['temperature'],
            spatial_bounds=settings.DEFAULT_BBOX,
            temporal_bounds=[
                datetime.now() - timedelta(days=365),
                datetime.now()
            ],
            depth_range=settings.DEFAULT_DEPTH_RANGE,
            query_type=QueryType.SPATIAL,
            filters={}
        )

# Global cloud query processor instance
query_processor = QueryProcessor()