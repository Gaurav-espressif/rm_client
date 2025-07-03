from typing import Dict, List, Optional, Union, Literal
from ..utils.api_client import ApiClient
import json
import logging

# Valid data types for time series
DataType = Literal["float", "int", "bool", "string", "array", "object"]

class TimeSeriesService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def _validate_data_type(self, data_type: str) -> None:
        """Validate that the data type is one of the allowed values"""
        valid_types = ["float", "int", "bool", "string", "array", "object"]
        if data_type not in valid_types:
            raise ValueError(f"Invalid data type '{data_type}'. Must be one of: {', '.join(valid_types)}")

    # User Time Series Operations
    def get_user_tsdata(self, node_id: str, param_name: str, aggregate: Optional[str] = None,
                       aggregation_interval: Optional[str] = None, differential: bool = False,
                       reset_on_negative: bool = False, desc_order: bool = False,
                       data_type: str = "float", week_start: str = "Monday",
                       start_time: Optional[int] = None, end_time: Optional[int] = None,
                       num_intervals: Optional[int] = None, start_id: Optional[str] = None,
                       num_records: Optional[int] = None, timezone: str = "UTC") -> Dict:
        """Get time series data for a node"""
        self._validate_data_type(data_type)
        
        endpoint = "/v1/user/nodes/tsdata"
        params = {
            "node_id": node_id,
            "param_name": param_name,
            "data_type": data_type,
            "week_start": week_start,
            "timezone": timezone
        }
        
        if aggregate:
            params["aggregate"] = aggregate
        if aggregation_interval:
            params["aggregation_interval"] = aggregation_interval
        if differential:
            params["differential"] = "true"
        if reset_on_negative:
            params["reset_on_negative"] = "true"
        if desc_order:
            params["desc_order"] = "true"
        if start_time:
            params["start_time"] = str(start_time)
        if end_time:
            params["end_time"] = str(end_time)
        if num_intervals:
            params["num_intervals"] = str(num_intervals)
        if start_id:
            params["start_id"] = start_id
        if num_records is not None:
            params["num_records"] = str(num_records)
            
        return self.api_client.get(endpoint, params=params)

    def get_user_simple_tsdata(self, node_id: str, param_name: str, data_type: str,
                             start_time: Optional[int] = None, end_time: Optional[int] = None,
                             start_id: Optional[str] = None, num_records: Optional[int] = None) -> Dict:
        """Get simple time series data for a node"""
        self._validate_data_type(data_type)
        
        endpoint = "/v1/user/nodes/simple_tsdata"
        params = {
            "node_id": node_id,
            "param_name": param_name,
            "data_type": data_type
        }
        
        if start_time:
            params["start_time"] = str(start_time)
        if end_time:
            params["end_time"] = str(end_time)
        if start_id:
            params["start_id"] = start_id
        if num_records is not None:
            params["num_records"] = str(num_records)
            
        return self.api_client.get(endpoint, params=params)

    # Admin Time Series Operations
    def get_admin_tsdata(self, node_id: str, param_name: str, aggregate: Optional[str] = None,
                        aggregation_interval: Optional[str] = None, differential: bool = False,
                        reset_on_negative: bool = False, desc_order: bool = False,
                        data_type: str = "float", week_start: str = "Monday",
                        start_time: Optional[int] = None, end_time: Optional[int] = None,
                        num_intervals: Optional[int] = None, start_id: Optional[str] = None,
                        num_records: Optional[int] = None, timezone: str = "UTC") -> Dict:
        """Get time series data for a node as admin"""
        self._validate_data_type(data_type)
        
        endpoint = "/v1/admin/nodes/tsdata"
        params = {
            "node_id": node_id,
            "param_name": param_name,
            "data_type": data_type,
            "week_start": week_start,
            "timezone": timezone
        }
        
        if aggregate:
            params["aggregate"] = aggregate
        if aggregation_interval:
            params["aggregation_interval"] = aggregation_interval
        if differential:
            params["differential"] = "true"
        if reset_on_negative:
            params["reset_on_negative"] = "true"
        if desc_order:
            params["desc_order"] = "true"
        if start_time:
            params["start_time"] = str(start_time)
        if end_time:
            params["end_time"] = str(end_time)
        if num_intervals:
            params["num_intervals"] = str(num_intervals)
        if start_id:
            params["start_id"] = start_id
        if num_records is not None:
            params["num_records"] = str(num_records)
            
        return self.api_client.get(endpoint, params=params)

    def get_admin_simple_tsdata(self, node_id: str, param_name: str, data_type: str,
                              start_time: Optional[int] = None, end_time: Optional[int] = None,
                              start_id: Optional[str] = None, num_records: Optional[int] = None) -> Dict:
        """Get simple time series data for a node as admin"""
        self._validate_data_type(data_type)
        
        endpoint = "/v1/admin/nodes/simple_tsdata"
        params = {
            "node_id": node_id,
            "param_name": param_name,
            "data_type": data_type
        }
        
        if start_time:
            params["start_time"] = str(start_time)
        if end_time:
            params["end_time"] = str(end_time)
        if start_id:
            params["start_id"] = start_id
        if num_records is not None:
            params["num_records"] = str(num_records)
            
        return self.api_client.get(endpoint, params=params) 