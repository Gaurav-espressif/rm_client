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
                return response if raw else []

            # Handle successful response
            if isinstance(response, dict):
                if "nodes" in response:
                    return response if raw else response["nodes"]
                return response if raw else []

            # Handle list response
            if isinstance(response, list):
                return {"nodes": response, "total": len(response)} if raw else response

            self.logger.warning(f"Unexpected response type: {type(response)}")
            return {} if raw else []
        except Exception as e:
            self.logger.error(f"Error in get_user_nodes: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            } if raw else []

    def get_node_config(self, node_id: str) -> Dict:
        """Get node configuration"""
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

    def update_node_metadata(
        self,
        node_id: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Update node metadata/tags"""
        endpoint = "/v1/user/nodes"
        params = {"node_id": node_id}
        payload = {}
        if tags:
            payload["tags"] = tags
        if metadata:
            payload["metadata"] = metadata
        return self.api_client.put(endpoint, params=params, json=payload)

    def delete_node_tags(self, node_id: str, tags: List[str]) -> Dict:
        """Delete tags from a node"""
        endpoint = "/v1/user/nodes"
        params = {"node_id": node_id}
        return self.api_client.delete(endpoint, params=params, json={"tags": tags})

    def map_user_node(
            self,
            node_id: str,
            secret_key: str,
            operation: str = "add"
    ) -> Dict:
        """Add or remove user node mapping"""
        endpoint = f"/v1/user/nodes/mapping"
        payload = {
            "node_id": node_id,
            "secret_key": secret_key,
            "operation": operation
        }
        return self.api_client.put(endpoint, json=payload)

    def get_mapping_status(
            self,
            request_id: str
    ) -> Dict:
        """Get status of user node mapping request"""
        endpoint = f"/v1/user/nodes/mapping"
        params = {"request_id": request_id}
        return self.api_client.get(endpoint, params=params)