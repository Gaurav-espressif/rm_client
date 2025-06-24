from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import json
import logging


class GroupingService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    # Admin Group Operations
    def create_admin_group(self, group_name: str, parent_group_id: Optional[str] = None,
                          nodes: Optional[List[str]] = None, description: Optional[str] = None,
                          group_type: Optional[str] = None, node_fw_version: Optional[str] = None,
                          node_model: Optional[str] = None, node_type: Optional[str] = None,
                          group_metadata: Optional[Dict] = None, custom_data: Optional[Dict] = None) -> Dict:
        """Create admin device group"""
        endpoint = "/v1/admin/node_group"
        payload = {
            "group_name": group_name
        }
        
        if parent_group_id:
            payload["parent_group_id"] = parent_group_id
        if nodes:
            payload["nodes"] = nodes
        if description:
            payload["description"] = description
        if group_type:
            payload["type"] = group_type
        if node_fw_version:
            payload["node_fw_version"] = node_fw_version
        if node_model:
            payload["node_model"] = node_model
        if node_type:
            payload["node_type"] = node_type
        if group_metadata:
            payload["group_metadata"] = group_metadata
        if custom_data:
            payload["custom_data"] = custom_data
            
        return self.api_client.post(endpoint, json=payload)

    def update_admin_group(self, group_id: str, group_name: Optional[str] = None,
                          group_type: Optional[str] = None, operation: Optional[str] = None,
                          nodes: Optional[List[str]] = None, description: Optional[str] = None,
                          group_metadata: Optional[Dict] = None, custom_data: Optional[Dict] = None,
                          regroup: bool = False) -> Dict:
        """Update admin device group"""
        endpoint = "/v1/admin/node_group"
        params = {"group_id": group_id}
        payload = {}
        
        if group_name:
            payload["group_name"] = group_name
        if group_type:
            payload["type"] = group_type
        if operation:
            payload["operation"] = operation
        if nodes:
            payload["nodes"] = nodes
        if description:
            payload["description"] = description
        if group_metadata:
            payload["group_metadata"] = group_metadata
        if custom_data:
            payload["custom_data"] = custom_data
        if regroup:
            payload["regroup"] = regroup
            
        return self.api_client.put(endpoint, json=payload, params=params)

    def get_admin_group(self, group_id: Optional[str] = None, group_name: Optional[str] = None,
                       node_details: bool = False, start_id: Optional[str] = None,
                       num_records: Optional[int] = None, node_model: Optional[str] = None,
                       node_type: Optional[str] = None, node_fw_version: Optional[str] = None) -> Dict:
        """Get admin device group details"""
        endpoint = "/v1/admin/node_group"
        params = {}
        
        if group_id:
            params["group_id"] = group_id
        if group_name:
            params["group_name"] = group_name
        if node_details:
            params["node_details"] = "true"
        if start_id:
            params["start_id"] = start_id
        if num_records:
            params["num_records"] = str(num_records)
        if node_model:
            params["node_model"] = node_model
        if node_type:
            params["node_type"] = node_type
        if node_fw_version:
            params["node_fw_version"] = node_fw_version
            
        return self.api_client.get(endpoint, params=params)

    def delete_admin_group(self, group_id: str) -> Dict:
        """Delete admin device group"""
        endpoint = "/v1/admin/node_group"
        params = {"group_id": group_id}
        return self.api_client.delete(endpoint, params=params)

    # User Group Operations
    def create_user_group(self, group_name: str, parent_group_id: Optional[str] = None,
                         nodes: Optional[List[str]] = None, description: Optional[str] = None,
                         group_metadata: Optional[Dict] = None, group_type: Optional[str] = None,
                         mutually_exclusive: bool = False, custom_data: Optional[Dict] = None,
                         is_matter: bool = False) -> Dict:
        """Create user device group or matter fabric"""
        endpoint = "/v1/user/node_group"
        payload = {
            "group_name": group_name
        }
        
        if parent_group_id:
            payload["parent_group_id"] = parent_group_id
        if nodes:
            payload["nodes"] = nodes
        if description:
            payload["description"] = description
        if group_metadata:
            payload["group_metadata"] = group_metadata
        if group_type:
            payload["type"] = group_type
        if mutually_exclusive:
            payload["mutually_exclusive"] = mutually_exclusive
        if custom_data:
            payload["custom_data"] = custom_data
        if is_matter:
            payload["is_matter"] = is_matter
            
        return self.api_client.post(endpoint, json=payload)

    def update_user_group(self, group_id: Optional[str] = None, group_name: Optional[str] = None,
                         operation: Optional[str] = None, group_type: Optional[str] = None,
                         mutually_exclusive: Optional[bool] = None, nodes: Optional[List[str]] = None,
                         description: Optional[str] = None, group_metadata: Optional[Dict] = None,
                         custom_data: Optional[Dict] = None, matter_controller: Optional[str] = None) -> Dict:
        """Update user device group or matter fabric"""
        endpoint = "/v1/user/node_group"
        params = {}
        payload = {}
        
        if group_id:
            params["group_id"] = group_id
        if matter_controller:
            params["matter_controller"] = matter_controller
            
        if group_name:
            payload["group_name"] = group_name
        if operation:
            payload["operation"] = operation
        if group_type:
            payload["type"] = group_type
        if mutually_exclusive is not None:
            payload["mutually_exclusive"] = mutually_exclusive
        if nodes:
            payload["nodes"] = nodes
        if description:
            payload["description"] = description
        if group_metadata:
            payload["group_metadata"] = group_metadata
        if custom_data:
            payload["custom_data"] = custom_data
            
        return self.api_client.put(endpoint, json=payload, params=params)

    def get_user_group(self, group_id: Optional[str] = None, group_name: Optional[str] = None,
                      node_list: bool = False, sub_groups: bool = False, start_id: Optional[str] = None,
                      num_records: Optional[int] = None, node_details: bool = False,
                      matter_node_list: bool = False, is_matter: bool = False,
                      fabric_details: bool = False) -> Dict:
        """Get user device group details"""
        endpoint = "/v1/user/node_group"
        params = {}
        
        if group_id:
            params["group_id"] = group_id
        if group_name:
            params["group_name"] = group_name
        if node_list:
            params["node_list"] = "true"
        if sub_groups:
            params["sub_groups"] = "true"
        if start_id:
            params["start_id"] = start_id
        if num_records:
            params["num_records"] = str(num_records)
        if node_details:
            params["node_details"] = "true"
        if matter_node_list:
            params["matter_node_list"] = "true"
        if is_matter:
            params["is_matter"] = "true"
        if fabric_details:
            params["fabric_details"] = "true"
            
        return self.api_client.get(endpoint, params=params)

    def delete_user_group(self, group_id: str, leave: bool = False, remove_sharing: bool = False,
                         user_name: Optional[str] = None) -> Dict:
        """Delete user device group or matter fabric"""
        endpoint = "/v1/user/node_group"
        params = {"group_id": group_id}
        
        if leave:
            params["leave"] = "true"
        if remove_sharing:
            params["remove_sharing"] = "true"
        if user_name:
            params["user_name"] = user_name
            
        return self.api_client.delete(endpoint, params=params)

    # Group Sharing Operations
    def share_group(self, groups: List[str], user_name: str, primary: bool = False,
                   metadata: Optional[Dict] = None) -> Dict:
        """Share groups or matter fabrics with another user"""
        endpoint = "/v1/user/node_group/sharing"
        payload = {
            "groups": groups,
            "user_name": user_name,
            "primary": primary
        }
        
        if metadata:
            payload["metadata"] = metadata
            
        return self.api_client.put(endpoint, json=payload)

    def get_group_sharing(self, group_id: Optional[str] = None, sub_groups: bool = False,
                         metadata: bool = False, parent_groups: bool = False) -> Dict:
        """Get group sharing details"""
        endpoint = "/v1/user/node_group/sharing"
        params = {}
        
        if group_id:
            params["group_id"] = group_id
        if sub_groups:
            params["sub_groups"] = "true"
        if metadata:
            params["metadata"] = "true"
        if parent_groups:
            params["parent_groups"] = "true"
            
        return self.api_client.get(endpoint, params=params)

    def get_sharing_requests(self, request_id: Optional[str] = None, primary_user: Optional[str] = None,
                           start_request_id: Optional[str] = None, start_user_name: Optional[str] = None,
                           num_records: Optional[int] = None) -> Dict:
        """Get group sharing requests"""
        endpoint = "/v1/user/node_group/sharing/requests"
        params = {}
        
        if request_id:
            params["request_id"] = request_id
        if primary_user:
            params["primary_user"] = primary_user
        if start_request_id:
            params["start_request_id"] = start_request_id
        if start_user_name:
            params["start_user_name"] = start_user_name
        if num_records:
            params["num_records"] = str(num_records)
            
        return self.api_client.get(endpoint, params=params)

    def delete_sharing_request(self, request_id: str) -> Dict:
        """Delete group sharing request"""
        endpoint = "/v1/user/node_group/sharing/requests"
        params = {"request_id": request_id}
        return self.api_client.delete(endpoint, params=params)

    def respond_to_sharing_request(self, request_id: str, accept: bool) -> Dict:
        """Accept or decline group sharing request"""
        endpoint = "/v1/user/node_group/sharing/requests"
        payload = {
            "request_id": request_id,
            "accept": accept
        }
        return self.api_client.put(endpoint, json=payload)

    def get_node_acl(self) -> Dict:
        """Get fabric Node ACLs"""
        endpoint = "/v1/user/node_group/node_acl"
        return self.api_client.get(endpoint)
