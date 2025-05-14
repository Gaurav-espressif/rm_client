from typing import Dict, List, Optional
from ..utils.api_client import ApiClient

class NodeService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_user_nodes(self) -> List[Dict]:
        """Get all nodes associated with the user"""
        endpoint = "/v1/user/nodes"
        return self.api_client.get(endpoint)

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