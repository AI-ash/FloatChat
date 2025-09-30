<<<<<<< HEAD
"""
Visualization service for creating charts and maps
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
import json
import numpy as np
import pandas as pd

from backend.models import Visualization, QueryType

logger = logging.getLogger(__name__)

class VisualizationService:
    """Service for creating visualizations from oceanographic data"""
    
    def __init__(self):
        pass
        
    async def initialize(self):
        """Initialize visualization service"""
        logger.info("Visualization service initialized")
    
    async def create_visualizations(
        self,
        data: List[Dict[str, Any]],
        query_type: QueryType,
        variables: List[str]
    ) -> List[Visualization]:
        """Create appropriate visualizations based on query type and data"""
        try:
            visualizations = []
            
            if not data:
                return visualizations
            
            # Create map visualization for spatial data
            if query_type in [QueryType.SPATIAL, QueryType.TRAJECTORY]:
                map_viz = await self._create_map_visualization(data, variables)
                if map_viz:
                    visualizations.append(map_viz)
            
            # Create time series plot for temporal data
            if query_type in [QueryType.TIMESERIES, QueryType.TREND]:
                timeseries_viz = await self._create_timeseries_visualization(data, variables)
                if timeseries_viz:
                    visualizations.append(timeseries_viz)
            
            # Create profile plot for depth data
            if query_type == QueryType.PROFILE:
                profile_viz = await self._create_profile_visualization(data, variables)
                if profile_viz:
                    visualizations.append(profile_viz)
            
            # Create comparison chart
            if query_type == QueryType.COMPARISON:
                comparison_viz = await self._create_comparison_visualization(data, variables)
                if comparison_viz:
                    visualizations.append(comparison_viz)
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            return []
    
    async def _create_map_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create interactive map visualization"""
        try:
            # Extract coordinates and values
            locations = []
            values = []
            
            for record in data:
                if 'latitude' in record and 'longitude' in record:
                    locations.append([record['latitude'], record['longitude']])
                    
                    # Get first available variable value
                    value = None
                    for var in variables:
                        if var in record.get('measurements', {}):
                            measurement = record['measurements'][var]
                            if isinstance(measurement, dict) and 'values' in measurement:
                                # Take surface value (first depth)
                                if measurement['values']:
                                    value = measurement['values'][0]
                                    break
                            elif isinstance(measurement, (int, float)):
                                value = measurement
                                break
                    
                    values.append(value if value is not None else 0)
            
            if not locations:
                return None
            
            # Create map configuration
            config = {
                "type": "scatter_mapbox",
                "lat": [loc[0] for loc in locations],
                "lon": [loc[1] for loc in locations],
                "mode": "markers",
                "marker": {
                    "size": 8,
                    "color": values,
                    "colorscale": "Viridis",
                    "showscale": True,
                    "colorbar": {
                        "title": variables[0] if variables else "Value"
                    }
                },
                "text": [f"Float: {data[i].get('float_id', 'Unknown')}<br>Value: {values[i]:.2f}" 
                        for i in range(len(values))],
                "hovertemplate": "%{text}<extra></extra>"
            }
            
            layout = {
                "mapbox": {
                    "style": "open-street-map",
                    "center": {
                        "lat": float(np.mean([loc[0] for loc in locations])),
                        "lon": float(np.mean([loc[1] for loc in locations]))
                    },
                    "zoom": 5
                },
                "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
                "height": 500
            }
            
            return Visualization(
                type="map",
                title=f"{variables[0].title()} Distribution" if variables else "Data Distribution",
                config={
                    "data": [config],
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating map visualization: {e}")
            return None
    
    async def _create_timeseries_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create time series plot"""
        try:
            # Group data by time
            time_series = {}
            
            for record in data:
                timestamp = record.get('timestamp')
                if not timestamp:
                    continue
                
                for var in variables:
                    if var in record.get('measurements', {}):
                        measurement = record['measurements'][var]
                        
                        # Extract surface value
                        value = None
                        if isinstance(measurement, dict) and 'values' in measurement:
                            if measurement['values']:
                                value = measurement['values'][0]  # Surface value
                        elif isinstance(measurement, (int, float)):
                            value = measurement
                        
                        if value is not None:
                            if var not in time_series:
                                time_series[var] = {'timestamps': [], 'values': []}
                            time_series[var]['timestamps'].append(timestamp)
                            time_series[var]['values'].append(value)
            
            if not time_series:
                return None
            
            # Create traces for each variable
            traces = []
            for var, data_series in time_series.items():
                traces.append({
                    "x": data_series['timestamps'],
                    "y": data_series['values'],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": var.title(),
                    "line": {"width": 2}
                })
            
            layout = {
                "title": f"Time Series: {', '.join([v.title() for v in variables])}",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Value"},
                "hovermode": "x unified",
                "height": 400
            }
            
            return Visualization(
                type="plot",
                title="Time Series Analysis",
                config={
                    "data": traces,
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating timeseries visualization: {e}")
            return None
    
    async def _create_profile_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create depth profile plot"""
        try:
            profiles = []
            
            for record in data:
                for var in variables:
                    if var in record.get('measurements', {}):
                        measurement = record['measurements'][var]
                        
                        if isinstance(measurement, dict) and 'depths' in measurement and 'values' in measurement:
                            depths = measurement['depths']
                            values = measurement['values']
                            
                            if depths and values and len(depths) == len(values):
                                profiles.append({
                                    "x": values,
                                    "y": depths,
                                    "type": "scatter",
                                    "mode": "lines+markers",
                                    "name": f"{var.title()} - Float {record.get('float_id', 'Unknown')}",
                                    "line": {"width": 2}
                                })
            
            if not profiles:
                return None
            
            layout = {
                "title": f"Depth Profiles: {', '.join([v.title() for v in variables])}",
                "xaxis": {"title": f"{variables[0].title()} Value" if variables else "Value"},
                "yaxis": {"title": "Depth (m)", "autorange": "reversed"},
                "hovermode": "closest",
                "height": 500
            }
            
            return Visualization(
                type="plot",
                title="Depth Profile Analysis",
                config={
                    "data": profiles,
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating profile visualization: {e}")
            return None
    
    async def _create_comparison_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create comparison chart"""
        try:
            if len(variables) < 2:
                return None
            
            # Extract values for comparison
            var1_values = []
            var2_values = []
            labels = []
            
            for record in data:
                measurements = record.get('measurements', {})
                
                val1 = None
                val2 = None
                
                # Get surface values for both variables
                if variables[0] in measurements:
                    m1 = measurements[variables[0]]
                    if isinstance(m1, dict) and 'values' in m1 and m1['values']:
                        val1 = m1['values'][0]
                    elif isinstance(m1, (int, float)):
                        val1 = m1
                
                if variables[1] in measurements:
                    m2 = measurements[variables[1]]
                    if isinstance(m2, dict) and 'values' in m2 and m2['values']:
                        val2 = m2['values'][0]
                    elif isinstance(m2, (int, float)):
                        val2 = m2
                
                if val1 is not None and val2 is not None:
                    var1_values.append(val1)
                    var2_values.append(val2)
                    labels.append(record.get('float_id', 'Unknown'))
            
            if not var1_values or not var2_values:
                return None
            
            trace = {
                "x": var1_values,
                "y": var2_values,
                "type": "scatter",
                "mode": "markers",
                "marker": {
                    "size": 8,
                    "color": "blue",
                    "opacity": 0.7
                },
                "text": labels,
                "hovertemplate": f"{variables[0].title()}: %{{x}}<br>{variables[1].title()}: %{{y}}<br>Float: %{{text}}<extra></extra>"
            }
            
            layout = {
                "title": f"{variables[0].title()} vs {variables[1].title()}",
                "xaxis": {"title": variables[0].title()},
                "yaxis": {"title": variables[1].title()},
                "hovermode": "closest",
                "height": 400
            }
            
            return Visualization(
                type="plot",
                title="Variable Comparison",
                config={
                    "data": [trace],
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating comparison visualization: {e}")
=======
"""
Visualization service for creating charts and maps
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
import json
import numpy as np
import pandas as pd

from backend.models import Visualization, QueryType

logger = logging.getLogger(__name__)

class VisualizationService:
    """Service for creating visualizations from oceanographic data"""
    
    def __init__(self):
        pass
        
    async def initialize(self):
        """Initialize visualization service"""
        logger.info("Visualization service initialized")
    
    async def create_visualizations(
        self,
        data: List[Dict[str, Any]],
        query_type: QueryType,
        variables: List[str]
    ) -> List[Visualization]:
        """Create appropriate visualizations based on query type and data"""
        try:
            visualizations = []
            
            if not data:
                return visualizations
            
            # Create map visualization for spatial data
            if query_type in [QueryType.SPATIAL, QueryType.TRAJECTORY]:
                map_viz = await self._create_map_visualization(data, variables)
                if map_viz:
                    visualizations.append(map_viz)
            
            # Create time series plot for temporal data
            if query_type in [QueryType.TIMESERIES, QueryType.TREND]:
                timeseries_viz = await self._create_timeseries_visualization(data, variables)
                if timeseries_viz:
                    visualizations.append(timeseries_viz)
            
            # Create profile plot for depth data
            if query_type == QueryType.PROFILE:
                profile_viz = await self._create_profile_visualization(data, variables)
                if profile_viz:
                    visualizations.append(profile_viz)
            
            # Create comparison chart
            if query_type == QueryType.COMPARISON:
                comparison_viz = await self._create_comparison_visualization(data, variables)
                if comparison_viz:
                    visualizations.append(comparison_viz)
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
            return []
    
    async def _create_map_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create interactive map visualization"""
        try:
            # Extract coordinates and values
            locations = []
            values = []
            
            for record in data:
                if 'latitude' in record and 'longitude' in record:
                    locations.append([record['latitude'], record['longitude']])
                    
                    # Get first available variable value
                    value = None
                    for var in variables:
                        if var in record.get('measurements', {}):
                            measurement = record['measurements'][var]
                            if isinstance(measurement, dict) and 'values' in measurement:
                                # Take surface value (first depth)
                                if measurement['values']:
                                    value = measurement['values'][0]
                                    break
                            elif isinstance(measurement, (int, float)):
                                value = measurement
                                break
                    
                    values.append(value if value is not None else 0)
            
            if not locations:
                return None
            
            # Create map configuration
            config = {
                "type": "scatter_mapbox",
                "lat": [loc[0] for loc in locations],
                "lon": [loc[1] for loc in locations],
                "mode": "markers",
                "marker": {
                    "size": 8,
                    "color": values,
                    "colorscale": "Viridis",
                    "showscale": True,
                    "colorbar": {
                        "title": variables[0] if variables else "Value"
                    }
                },
                "text": [f"Float: {data[i].get('float_id', 'Unknown')}<br>Value: {values[i]:.2f}" 
                        for i in range(len(values))],
                "hovertemplate": "%{text}<extra></extra>"
            }
            
            layout = {
                "mapbox": {
                    "style": "open-street-map",
                    "center": {
                        "lat": float(np.mean([loc[0] for loc in locations])),
                        "lon": float(np.mean([loc[1] for loc in locations]))
                    },
                    "zoom": 5
                },
                "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
                "height": 500
            }
            
            return Visualization(
                type="map",
                title=f"{variables[0].title()} Distribution" if variables else "Data Distribution",
                config={
                    "data": [config],
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating map visualization: {e}")
            return None
    
    async def _create_timeseries_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create time series plot"""
        try:
            # Group data by time
            time_series = {}
            
            for record in data:
                timestamp = record.get('timestamp')
                if not timestamp:
                    continue
                
                for var in variables:
                    if var in record.get('measurements', {}):
                        measurement = record['measurements'][var]
                        
                        # Extract surface value
                        value = None
                        if isinstance(measurement, dict) and 'values' in measurement:
                            if measurement['values']:
                                value = measurement['values'][0]  # Surface value
                        elif isinstance(measurement, (int, float)):
                            value = measurement
                        
                        if value is not None:
                            if var not in time_series:
                                time_series[var] = {'timestamps': [], 'values': []}
                            time_series[var]['timestamps'].append(timestamp)
                            time_series[var]['values'].append(value)
            
            if not time_series:
                return None
            
            # Create traces for each variable
            traces = []
            for var, data_series in time_series.items():
                traces.append({
                    "x": data_series['timestamps'],
                    "y": data_series['values'],
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": var.title(),
                    "line": {"width": 2}
                })
            
            layout = {
                "title": f"Time Series: {', '.join([v.title() for v in variables])}",
                "xaxis": {"title": "Time"},
                "yaxis": {"title": "Value"},
                "hovermode": "x unified",
                "height": 400
            }
            
            return Visualization(
                type="plot",
                title="Time Series Analysis",
                config={
                    "data": traces,
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating timeseries visualization: {e}")
            return None
    
    async def _create_profile_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create depth profile plot"""
        try:
            profiles = []
            
            for record in data:
                for var in variables:
                    if var in record.get('measurements', {}):
                        measurement = record['measurements'][var]
                        
                        if isinstance(measurement, dict) and 'depths' in measurement and 'values' in measurement:
                            depths = measurement['depths']
                            values = measurement['values']
                            
                            if depths and values and len(depths) == len(values):
                                profiles.append({
                                    "x": values,
                                    "y": depths,
                                    "type": "scatter",
                                    "mode": "lines+markers",
                                    "name": f"{var.title()} - Float {record.get('float_id', 'Unknown')}",
                                    "line": {"width": 2}
                                })
            
            if not profiles:
                return None
            
            layout = {
                "title": f"Depth Profiles: {', '.join([v.title() for v in variables])}",
                "xaxis": {"title": f"{variables[0].title()} Value" if variables else "Value"},
                "yaxis": {"title": "Depth (m)", "autorange": "reversed"},
                "hovermode": "closest",
                "height": 500
            }
            
            return Visualization(
                type="plot",
                title="Depth Profile Analysis",
                config={
                    "data": profiles,
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating profile visualization: {e}")
            return None
    
    async def _create_comparison_visualization(
        self,
        data: List[Dict[str, Any]],
        variables: List[str]
    ) -> Optional[Visualization]:
        """Create comparison chart"""
        try:
            if len(variables) < 2:
                return None
            
            # Extract values for comparison
            var1_values = []
            var2_values = []
            labels = []
            
            for record in data:
                measurements = record.get('measurements', {})
                
                val1 = None
                val2 = None
                
                # Get surface values for both variables
                if variables[0] in measurements:
                    m1 = measurements[variables[0]]
                    if isinstance(m1, dict) and 'values' in m1 and m1['values']:
                        val1 = m1['values'][0]
                    elif isinstance(m1, (int, float)):
                        val1 = m1
                
                if variables[1] in measurements:
                    m2 = measurements[variables[1]]
                    if isinstance(m2, dict) and 'values' in m2 and m2['values']:
                        val2 = m2['values'][0]
                    elif isinstance(m2, (int, float)):
                        val2 = m2
                
                if val1 is not None and val2 is not None:
                    var1_values.append(val1)
                    var2_values.append(val2)
                    labels.append(record.get('float_id', 'Unknown'))
            
            if not var1_values or not var2_values:
                return None
            
            trace = {
                "x": var1_values,
                "y": var2_values,
                "type": "scatter",
                "mode": "markers",
                "marker": {
                    "size": 8,
                    "color": "blue",
                    "opacity": 0.7
                },
                "text": labels,
                "hovertemplate": f"{variables[0].title()}: %{{x}}<br>{variables[1].title()}: %{{y}}<br>Float: %{{text}}<extra></extra>"
            }
            
            layout = {
                "title": f"{variables[0].title()} vs {variables[1].title()}",
                "xaxis": {"title": variables[0].title()},
                "yaxis": {"title": variables[1].title()},
                "hovermode": "closest",
                "height": 400
            }
            
            return Visualization(
                type="plot",
                title="Variable Comparison",
                config={
                    "data": [trace],
                    "layout": layout
                }
            )
            
        except Exception as e:
            logger.error(f"Error creating comparison visualization: {e}")
>>>>>>> 5347d1d (Initial commit: FloatChat AI-Powered ARGO Data System)
            return None