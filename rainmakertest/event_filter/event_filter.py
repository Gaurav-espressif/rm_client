from typing import Dict, List, Optional, Union, Literal
from ..utils.api_client import ApiClient
import json
import logging

# Valid entity types
EntityType = Literal["User", "Node", "System"]

class EventFilterService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def _validate_entity_type(self, entity_type: str) -> None:
        """Validate that the entity type is one of the allowed values"""
        valid_types = ["User", "Node", "System"]
        if entity_type not in valid_types:
            raise ValueError(f"Invalid entity type '{entity_type}'. Must be one of: {', '.join(valid_types)}")

    # Admin Event Filter Operations
    def create_admin_event_filter(self, event_type: str, entity_id: str, entity_type: str,
                                enabled: bool, enabled_for_integrations: Optional[List[str]] = None) -> Dict:
        """Create a new event filter as admin"""
        self._validate_entity_type(entity_type)
        
        endpoint = "/v1/admin/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "enabled": enabled
        }
        
        if enabled_for_integrations:
            data["enabled_for_integrations"] = enabled_for_integrations
            
        return self.api_client.post(endpoint, json=data)

    def update_admin_event_filter(self, event_type: str, entity_id: str, entity_type: str,
                                enabled: bool, enabled_for_integrations: Optional[List[str]] = None) -> Dict:
        """Update an event filter as admin"""
        self._validate_entity_type(entity_type)
        
        endpoint = "/v1/admin/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "enabled": enabled
        }
        
        if enabled_for_integrations:
            data["enabled_for_integrations"] = enabled_for_integrations
            
        return self.api_client.put(endpoint, json=data)

    def get_admin_event_filter(self, event_type: Optional[str] = None,
                             entity_type: Optional[str] = None,
                             entity_id: Optional[str] = None) -> Dict:
        """Get event filter information as admin"""
        if entity_type:
            self._validate_entity_type(entity_type)
        
        endpoint = "/v1/admin/event_filter"
        params = {}
        
        if event_type:
            params["event_type"] = event_type
        if entity_type:
            params["entity_type"] = entity_type
        if entity_id:
            params["entity_id"] = entity_id
            
        return self.api_client.get(endpoint, params=params)

    def delete_admin_event_filter(self, event_type: str, entity_id: str, entity_type: str) -> Dict:
        """Delete an event filter as admin"""
        self._validate_entity_type(entity_type)
        
        endpoint = "/v1/admin/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id,
            "entity_type": entity_type
        }
            
        return self.api_client.delete(endpoint, json=data)

    # User Event Filter Operations
    def create_user_event_filter(self, event_type: str, entity_id: str, entity_type: str,
                               enabled: bool, enabled_for_integrations: Optional[List[str]] = None) -> Dict:
        """Create a new event filter as user"""
        self._validate_entity_type(entity_type)
        
        endpoint = "/v1/user/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "enabled": enabled
        }
        
        if enabled_for_integrations:
            data["enabled_for_integrations"] = enabled_for_integrations
            
        return self.api_client.post(endpoint, json=data)

    def update_user_event_filter(self, event_type: str, entity_id: str, entity_type: str,
                               enabled: bool, enabled_for_integrations: Optional[List[str]] = None) -> Dict:
        """Update an event filter as user"""
        self._validate_entity_type(entity_type)
        
        endpoint = "/v1/user/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "enabled": enabled
        }
        
        if enabled_for_integrations:
            data["enabled_for_integrations"] = enabled_for_integrations
            
        return self.api_client.put(endpoint, json=data)

    def get_user_event_filter(self, event_type: Optional[str] = None,
                            entity_type: Optional[str] = None,
                            entity_id: Optional[str] = None) -> Dict:
        """Get event filter information as user"""
        if entity_type:
            self._validate_entity_type(entity_type)
        
        endpoint = "/v1/user/event_filter"
        params = {}
        
        if event_type:
            params["event_type"] = event_type
        if entity_type:
            params["entity_type"] = entity_type
        if entity_id:
            params["entity_id"] = entity_id
            
        return self.api_client.get(endpoint, params=params)

    def delete_user_event_filter(self, event_type: str, entity_id: str) -> Dict:
        """Delete an event filter as user"""
        endpoint = "/v1/user/event_filter"
        data = {
            "event_type": event_type,
            "entity_id": entity_id
        }
            
        return self.api_client.delete(endpoint, json=data)
