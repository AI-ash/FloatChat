"""
Cloud LLM service for natural language processing
"""
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

# Cloud AI Services
from openai import AsyncOpenAI
from groq import AsyncGroq
import cohere
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser

from config.settings import settings
from backend.models import ParsedQuery, QueryType

logger = logging.getLogger(__name__)

class QueryOutputParser(BaseOutputParser):
    """Parse LLM output into structured query parameters"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback to regex parsing
            result = {}
            
            # Extract variables
            var_match = re.search(r'variables?[:\s]+\[([^\]]+)\]', text, re.IGNORECASE)
            if var_match:
                variables = [v.strip().strip('"\'') for v in var_match.group(1).split(',')]
                result['variables'] = variables
            
            # Extract spatial bounds
            spatial_match = re.search(r'spatial[:\s]+\[([^\]]+)\]', text, re.IGNORECASE)
            if spatial_match:
                bounds = [float(x.strip()) for x in spatial_match.group(1).split(',')]
                result['spatial_bounds'] = bounds
            
            # Extract temporal bounds
            temporal_match = re.search(r'temporal[:\s]+\[([^\]]+)\]', text, re.IGNORECASE)
            if temporal_match:
                dates = temporal_match.group(1).split(',')
                result['temporal_bounds'] = [d.strip().strip('"\'') for d in dates]
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing LLM output: {e}")
            return {}

class LLMService:
    """Cloud-based LLM service for natural language processing"""
    
    def __init__(self):
        self.openai_client = None
        self.groq_client = None
        self.cohere_client = None
        
    async def initialize(self):
        """Initialize cloud LLM services"""
        try:
            # Initialize OpenAI client
            if settings.OPENAI_API_KEY:
                self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            
            # Initialize Groq client (Fast LLaMA inference)
            if settings.GROQ_API_KEY:
                self.groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            
            # Initialize Cohere client
            if settings.COHERE_API_KEY:
                self.cohere_client = cohere.AsyncClient(api_key=settings.COHERE_API_KEY)
            
            logger.info("Cloud LLM services initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LLM service: {e}")
            raise
    
    async def parse_query(self, query: str) -> ParsedQuery:
        """Parse natural language query using cloud LLM"""
        try:
            # Get available variables and regions
            available_variables = self._get_available_variables()
            regions = self._get_predefined_regions()
            
            # Create parsing prompt
            prompt = self._get_query_parsing_template().format(
                query=query,
                available_variables=available_variables,
                regions=regions
            )
            
            # Use Groq for fast inference (or fallback to OpenAI)
            if self.groq_client:
                response = await self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=1000
                )
                parsed_text = response.choices[0].message.content
            elif self.openai_client:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=1000
                )
                parsed_text = response.choices[0].message.content
            else:
                raise Exception("No LLM service available")
            
            # Parse the response
            parsed_result = QueryOutputParser().parse(parsed_text)
            
            # Convert to ParsedQuery model
            return self._convert_to_parsed_query(parsed_result, query)
            
        except Exception as e:
            logger.error(f"Error parsing query: {e}")
            return self._get_default_query(query)
    
    async def generate_response(
        self, 
        query: str, 
        data_summary: Dict[str, Any], 
        visualizations: List[Dict[str, Any]]
    ) -> str:
        """Generate natural language response using cloud LLM"""
        try:
            prompt = self._get_response_template().format(
                query=query,
                data_summary=json.dumps(data_summary, default=str),
                visualizations=json.dumps(visualizations, default=str)
            )
            
            # Use Groq for fast response generation
            if self.groq_client:
                response = await self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            elif self.openai_client:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            else:
                return f"I found {data_summary.record_count} records matching your query about oceanographic data."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I found {data_summary.record_count} records matching your query about oceanographic data."
    
    def _get_query_parsing_template(self) -> str:
        """Get prompt template for query parsing"""
        return """
You are an expert oceanographer helping users query ARGO float data. 
Parse the following natural language query into structured parameters.

Available variables: {available_variables}
Available regions: {regions}

User query: "{query}"

Extract the following information and return as JSON:
{{
    "variables": ["list of oceanographic variables requested"],
    "spatial_bounds": [min_longitude, min_latitude, max_longitude, max_latitude],
    "temporal_bounds": ["start_date", "end_date"],
    "depth_range": [min_depth_meters, max_depth_meters],
    "query_type": "profile|timeseries|spatial|trajectory|trend|comparison",
    "filters": {{"any additional filters"}}
}}

Guidelines:
- For location names, convert to approximate coordinates
- For relative time ("last 10 years"), calculate actual dates
- Default depth range is 0-2000m if not specified
- Default spatial bounds cover Indian Ocean region if not specified
- Infer query type from the request (profile for single location, timeseries for trends over time, etc.)

Return only the JSON object.
"""
    
    def _get_response_template(self) -> str:
        """Get prompt template for response generation"""
        return """
You are an expert oceanographer providing insights about ARGO float data.
Generate a natural, informative response to the user's query.

User query: "{query}"
Data summary: {data_summary}
Available visualizations: {visualizations}

Provide a response that:
1. Directly answers the user's question
2. Highlights key findings from the data
3. Mentions the data sources and quality
4. Suggests relevant visualizations
5. Uses accessible language appropriate for the user level

Keep the response concise but informative, around 2-3 paragraphs.
"""
    
    def _get_available_variables(self) -> List[str]:
        """Get list of available oceanographic variables"""
        return [
            "temperature", "salinity", "pressure", "oxygen", 
            "chlorophyll", "nitrate", "ph", "density"
        ]
    
    def _get_predefined_regions(self) -> Dict[str, List[float]]:
        """Get predefined geographic regions"""
        return {
            "Bay of Bengal": [80.0, 5.0, 100.0, 25.0],
            "Arabian Sea": [60.0, 8.0, 80.0, 25.0],
            "Indian Ocean": [40.0, -40.0, 120.0, 30.0],
            "Equatorial Indian Ocean": [50.0, -10.0, 100.0, 10.0]
        }
    
    def _convert_to_parsed_query(self, parsed_result: Dict[str, Any], original_query: str) -> ParsedQuery:
        """Convert parsed result to ParsedQuery model"""
        try:
            # Handle temporal bounds
            temporal_bounds = []
            if 'temporal_bounds' in parsed_result:
                for date_str in parsed_result['temporal_bounds']:
                    if isinstance(date_str, str):
                        # Parse relative dates
                        if 'last' in date_str.lower() and 'year' in date_str.lower():
                            years = int(re.search(r'\d+', date_str).group())
                            temporal_bounds = [
                                datetime.now() - timedelta(days=years*365),
                                datetime.now()
                            ]
                            break
                        else:
                            # Try to parse absolute date
                            try:
                                temporal_bounds.append(datetime.fromisoformat(date_str))
                            except:
                                pass
            
            # Default temporal bounds if not specified
            if not temporal_bounds:
                temporal_bounds = [
                    datetime.now() - timedelta(days=365),  # Last year
                    datetime.now()
                ]
            
            return ParsedQuery(
                variables=parsed_result.get('variables', ['temperature']),
                spatial_bounds=parsed_result.get('spatial_bounds', settings.DEFAULT_BBOX),
                temporal_bounds=temporal_bounds,
                depth_range=parsed_result.get('depth_range', settings.DEFAULT_DEPTH_RANGE),
                query_type=QueryType(parsed_result.get('query_type', 'spatial')),
                filters=parsed_result.get('filters', {})
            )
            
        except Exception as e:
            logger.error(f"Error converting parsed result: {e}")
            return self._get_default_query(original_query)
    
    def _get_default_query(self, query: str) -> ParsedQuery:
        """Get default query parameters"""
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