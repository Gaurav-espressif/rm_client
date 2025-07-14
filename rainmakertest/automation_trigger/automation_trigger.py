from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class AutomationTriggerService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def create_automation_trigger(self, name: str, event_type: str,
                                events: List[Dict], actions: List[Dict],
                                node_id: Optional[str] = None,
                                metadata: Optional[Union[str, Dict]] = None,
                                location: Optional[Dict] = None,
                                event_operator: Optional[str] = None,
                                retrigger: bool = False) -> Dict:
        """Create a new automation trigger"""
        endpoint = "/v1/user/node_automation"
        data = {
            "name": name,
            "event_type": event_type,
            "events": events,
            "actions": actions,
            "retrigger": retrigger
        }

        # Add optional fields if provided
        if node_id:
            data["node_id"] = node_id
        if metadata:
            data["metadata"] = metadata
        if location:
            data["location"] = location
        if event_operator:
            data["event_operator"] = event_operator

        return self.api_client.post(endpoint, json=data)

    def update_automation_trigger(self, automation_id: str, name: Optional[str] = None,
                                enabled: Optional[bool] = None,
                                events: Optional[List[Dict]] = None,
                                actions: Optional[List[Dict]] = None,
                                event_operator: Optional[str] = None,
                                retrigger: Optional[bool] = None) -> Dict:
        """Update an existing automation trigger"""
        endpoint = f"/v1/user/node_automation"
        params = {"automation_id": automation_id}
        data = {}

        # Add optional fields if provided
        if name is not None:
            data["name"] = name
        if enabled is not None:
            data["enabled"] = enabled
        if events is not None:
            data["events"] = events
        if actions is not None:
            data["actions"] = actions
        if event_operator is not None:
            data["event_operator"] = event_operator
        if retrigger is not None:
            data["retrigger"] = retrigger

        return self.api_client.put(endpoint, params=params, json=data)

    def get_automation_trigger(self, automation_id: Optional[str] = None,
                             node_id: Optional[str] = None,
                             start_id: Optional[str] = None,
                             num_records: Optional[str] = None) -> Dict:
        """Get automation trigger(s)"""
        endpoint = "/v1/user/node_automation"
        params = {}

        # Add optional query parameters
        if automation_id:
            params["automation_id"] = automation_id
        if node_id:
            params["node_id"] = node_id
        if start_id:
            params["start_id"] = start_id
        if num_records:
            params["num_records"] = num_records

        return self.api_client.get(endpoint, params=params)

    def delete_automation_trigger(self, automation_id: str) -> Dict:
        """Delete an automation trigger"""
        endpoint = "/v1/user/node_automation"
        params = {"automation_id": automation_id}
        return self.api_client.delete(endpoint, params=params)
