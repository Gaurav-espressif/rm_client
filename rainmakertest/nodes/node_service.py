from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import json
import logging


class NodeService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_user_nodes(self, raw: bool = False) -> Union[List[Dict], Dict]:
        """Get all nodes associated with the user"""
        endpoint = "/v1/user/nodes"
        
        try:
            self.logger.debug("Fetching user nodes...")
            response = self.api_client.get(endpoint)
            self.logger.debug(f"Raw API response: {response} (type: {type(response)})")

            # Handle error response
            if isinstance(response, dict) and response.get("status") == "failure":
                self.logger.error(f"API returned error: {response}")
                return {
                    "status": "error",
                    "response": None,
                    "error": response.get("message", "Unknown error")
                }

            # Handle successful response
            if isinstance(response, dict):
                if "nodes" in response:
                    return {
                        "status": "success",
                        "response": {
                            "nodes": response["nodes"],
                            "total": len(response["nodes"])
                        },
                        "error": None
                    }
                return {
                    "status": "success",
                    "response": {
                        "nodes": [],
                        "total": 0
                    },
                    "error": None
                }

            # Handle list response
            if isinstance(response, list):
                return {
                    "status": "success",
                    "response": {
                        "nodes": response,
                        "total": len(response)
                    },
                    "error": None
                }

            self.logger.warning(f"Unexpected response type: {type(response)}")
            return {
                "status": "success",
                "response": {
                    "nodes": [],
                    "total": 0
                },
                "error": None
            }
        except Exception as e:
            self.logger.error(f"Error in get_user_nodes: {str(e)}")
            return {
                "status": "error",
                "response": None,
                "error": str(e)
            }

    def get_node_config(self, node_id: str) -> Dict:
        """
        Get node configuration"""
        endpoint = "/v1/user/nodes/config"
        params = {"node_id": node_id}
        response = self.api_client.get(endpoint, params=params)
        # Check if response is an error dict from api_client
        if isinstance(response, dict) and response.get("status") == "failure":
            return response # Return the error dict
        if isinstance(response, dict) and 'config' in response:
            return response['config']
        return response or {}

    def get_node_status(self, node_id: str) -> Dict:
        """Get node online/offline status"""
        endpoint = "/v1/user/nodes/status"
        params = {"node_id": node_id}
        response = self.api_client.get(endpoint, params=params)

        # Check if response is an error dict from api_client
        if isinstance(response, dict) and response.get("status") == "failure":
            return response # Return the error dict

        # Handle the connectivity response format
        if isinstance(response, dict):
            if 'connectivity' in response and isinstance(response['connectivity'], dict):
                connected = response['connectivity'].get('connected', None)
                if connected is not None:
                    return {'status': 'online' if connected else 'offline'}

        return {'status': 'unknown'}

    def update_node_metadata(self, node_id: str, metadata: Dict) -> Dict:
        """Update node metadata or tags"""
        endpoint = "/v1/user/nodes"
        params = {"node_id": node_id}
        return self.api_client.put(endpoint, json=metadata, params=params)

    def delete_node_tags(self, node_id: str, tags: List[str]) -> Dict:
        """Delete tags from a node"""
        endpoint = "/v1/user/nodes"
        params = {"node_id": node_id}
        return self.api_client.delete(endpoint, json={"tags": tags}, params=params)

    def map_user_node(self, node_id: str, secret_key: str, operation: str) -> dict:
        if operation not in ['map', 'unmap']:
            return {
                "status": "failure",
                "error_code": 400,
                "description": "Invalid operation specified. Valid operations are 'map' or 'unmap'"
            }

        endpoint = "/v1/user/nodes/mapping"
        payload = {
            "node_id": node_id,
            "secret_key": secret_key,
            "operation": "add" if operation == "map" else "remove"
        }
        
        response = self.api_client.put(endpoint, json=payload)
        return response

    def get_mapping_status(self, request_id: str) -> dict:
        """
        Check the status of a node mapping request
        
        Args:
            request_id: The request ID from the mapping operation
            
        Returns:
            dict: Status response
        """
        endpoint = "/v1/user/nodes/mapping"
        params = {"request_id": request_id}
        return self.api_client.get(endpoint, params=params)