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
        return self.api_client.get(endpoint)

    def get_node_config(self, node_id: str) -> Dict:
        """Get node configuration"""
        endpoint = "/v1/user/nodes/config"
        params = {"node_id": node_id}
        return self.api_client.get(endpoint, params=params)

    def get_node_status(self, node_id: str) -> Dict:
        """Get node online/offline status"""
        endpoint = "/v1/user/nodes/status"
        params = {"node_id": node_id}
        return self.api_client.get(endpoint, params=params)

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
        """Map or unmap a node"""
        if operation not in ['map', 'unmap']:
            return {
                "status": "failure",
                "description": "Invalid operation specified. Valid operations are 'map' or 'unmap'",
                "error_code": 400
            }

        endpoint = "/v1/user/nodes/mapping"
        payload = {
            "node_id": node_id,
            "secret_key": secret_key,
            "operation": "add" if operation == "map" else "remove"
        }
        return self.api_client.put(endpoint, json=payload)

    def get_mapping_status(self, request_id: str) -> dict:
        """Check the status of a node mapping request"""
        endpoint = "/v1/user/nodes/mapping"
        params = {"request_id": request_id}
        return self.api_client.get(endpoint, params=params)