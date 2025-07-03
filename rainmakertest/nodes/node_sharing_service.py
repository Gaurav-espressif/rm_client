from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class NodeSharingService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def share_nodes(
        self,
        nodes: List[str],
        user_name: str,
        primary: bool = False,
        metadata: Optional[Dict] = None,
        version: str = "v1"
    ) -> Dict:
        """Share nodes with another user"""
        endpoint = f"/{version}/user/nodes/sharing"
        payload = {
            "nodes": nodes,
            "user_name": user_name,
            "primary": primary
        }
        if metadata:
            payload["metadata"] = metadata
        return self.api_client.put(endpoint, json=payload)

    def respond_to_request(
        self,
        request_id: str,
        accept: bool,
        version: str = "v1"
    ) -> Dict:
        """Accept or decline a node sharing request"""
        endpoint = f"/{version}/user/nodes/sharing"
        payload = {
            "accept": accept,
            "request_id": request_id
        }
        self.logger.debug(f"Sending request to {endpoint} with payload: {payload}")
        return self.api_client.put(endpoint, json=payload)

    def get_sharing_info(
        self,
        node_id: Optional[str] = None,
        version: str = "v1"
    ) -> Dict:
        """Get node sharing information"""
        endpoint = f"/{version}/user/nodes/sharing"
        params = {}
        if node_id:
            params["node_id"] = node_id
        return self.api_client.get(endpoint, params=params)

    def get_sharing_requests(
        self,
        request_id: Optional[str] = None,
        primary_user: Optional[str] = None,
        start_request_id: Optional[str] = None,
        version: str = "v1"
    ) -> Dict:
        """Get node sharing requests"""
        endpoint = f"/{version}/user/nodes/sharing/requests"
        params = {}
        if request_id:
            params["request_id"] = request_id
        if primary_user:
            params["primary_user"] = primary_user
        if start_request_id:
            params["start_request_id"] = start_request_id
        return self.api_client.get(endpoint, params=params)

    def unshare_nodes(
        self,
        nodes: List[str],
        user_name: str,
        version: str = "v1"
    ) -> Dict:
        """Unshare nodes with another user"""
        endpoint = f"/{version}/user/nodes/sharing"
        params = {
            "nodes": ",".join(nodes),
            "user_name": user_name
        }
        self.logger.debug(f"Sending unshare request to {endpoint} with params: {params}")
        return self.api_client.delete(endpoint, params=params)

    def transfer_nodes(
        self,
        nodes: List[str],
        user_name: str,
        metadata: Optional[Dict] = None,
        new_role: Optional[str] = None,
        version: str = "v1"
    ) -> Dict:
        
        endpoint = f"/{version}/user/nodes/sharing"
        payload = {
            "nodes": nodes,
            "user_name": user_name,
            "transfer": True
        }
        if metadata:
            payload["metadata"] = metadata
        if new_role:
            payload["new_role"] = new_role
        self.logger.debug(f"Sending transfer request to {endpoint} with payload: {payload}")
        return self.api_client.put(endpoint, json=payload) 
