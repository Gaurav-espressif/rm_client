from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class ExternalApiPassthroughService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_passthrough_config(self, service_id: Optional[str] = None,
                              service_name: Optional[str] = None,
                              start_id: Optional[str] = None,
                              num_records: int = 30) -> Dict:
        """Fetches external API configurations
        
        Args:
            service_id: Optional service ID to fetch specific service
            service_name: Optional service name prefix to filter services
            start_id: Optional start ID for pagination
            num_records: Number of records to fetch (max 30)
        """
        endpoint = "/v1/user/passthrough/config"
        params = {"num_records": min(num_records, 30)}  # Ensure max value of 30
        
        # Add optional query parameters
        if service_id:
            params["service_id"] = service_id
        if service_name:
            params["service_name"] = service_name
        if start_id:
            params["start_id"] = start_id
            
        return self.api_client.get(endpoint, params=params)

    def get_passthrough_data(self, service_id: str,
                            query_params_json: Optional[str] = None,
                            headers_json: Optional[str] = None,
                            path_params_string: Optional[str] = None) -> Dict:
        """Retrieves data from external API via GET request
        
        Args:
            service_id: Service ID to call
            query_params_json: Optional JSON string of query parameters
            headers_json: Optional JSON string of headers
            path_params_string: Optional path parameters string
        """
        endpoint = "/v1/user/passthrough"
        params = {"service_id": service_id}
        
        # Add optional query parameters
        if query_params_json:
            params["query_params_json"] = query_params_json
        if headers_json:
            params["headers_json"] = headers_json
        if path_params_string:
            params["path_params_string"] = path_params_string
            
        return self.api_client.get(endpoint, params=params)

    def post_passthrough_data(self, service_id: str,
                             query_params_json: Optional[str] = None,
                             headers_json: Optional[str] = None,
                             path_params_string: Optional[str] = None,
                             body_json: Optional[str] = None) -> Dict:
        """Makes a POST request to an external API endpoint
        
        Args:
            service_id: Service ID to call
            query_params_json: Optional JSON string of query parameters
            headers_json: Optional JSON string of headers
            path_params_string: Optional path parameters string
            body_json: Optional JSON string for request body
        """
        endpoint = "/v1/user/passthrough"
        params = {"service_id": service_id}
        data = {}
        
        # Add optional query parameters
        if query_params_json:
            params["query_params_json"] = query_params_json
        if headers_json:
            params["headers_json"] = headers_json
        if path_params_string:
            params["path_params_string"] = path_params_string
        if body_json:
            data["body_json"] = body_json
            
        return self.api_client.post(endpoint, params=params, json=data)
