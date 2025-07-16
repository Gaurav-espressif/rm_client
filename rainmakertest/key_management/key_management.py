from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class KeyManagementService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def create_key(self, key_name: str, key_spec: str,
                   description: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> Dict:
        """Create a new key
        
        Args:
            key_name: Name of the key (max 256 chars, alphanumeric, /, _, -)
            key_spec: Key specification (ECDSA-P256 or RSA-3072)
            description: Optional description for the key
            tags: Optional list of tags in format ["key:val"]
        """
        endpoint = "/v1/admin/key"
        data = {
            "key_name": key_name,
            "key_spec": key_spec
        }
        
        # Add optional fields if provided
        if description:
            data["description"] = description
        if tags:
            data["tags"] = tags
            
        return self.api_client.post(endpoint, json=data)

    def get_key(self, key_name: Optional[str] = None) -> Dict:
        """Get details and digest of the key
        
        Args:
            key_name: Optional name of the key. If not specified, returns all keys for current user
        """
        endpoint = "/v1/admin/key"
        params = {}
        
        if key_name:
            params["key_name"] = key_name
            
        return self.api_client.get(endpoint, params=params)
