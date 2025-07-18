from typing import Dict, List, Optional, Union, Literal
from ..utils.api_client import ApiClient
import json
import logging

class RolePolicyService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    # Policy Operations
    def create_policy(self, policy_name: str, policy_json: Dict) -> Dict:
        """Create a new policy"""
        endpoint = "/v1/admin/policy"
        data = {
            "policy_name": policy_name,
            "policy_json": policy_json
        }
        
        return self.api_client.post(endpoint, json=data)

    def update_policy(self, policy_name: str, policy_json: Dict) -> Dict:
        """Update an existing policy"""
        endpoint = f"/v1/admin/policy"
        params = {
            "policy_name": policy_name
        }
        data = {
            "policy_json": policy_json
        }
        
        return self.api_client.put(endpoint, params=params, json=data)

    def get_policy(self, policy_name: Optional[str] = None) -> Dict:
        """Get policy information"""
        endpoint = "/v1/admin/policy"
        params = {}
        
        if policy_name:
            params["policy_name"] = policy_name
            
        return self.api_client.get(endpoint, params=params)

    def delete_policy(self, policy_name: str) -> Dict:
        """Delete a policy"""
        endpoint = "/v1/admin/policy"
        params = {
            "policy_name": policy_name
        }
            
        return self.api_client.delete(endpoint, params=params)

    # Role Operations
    def create_role(self, role_name: str, policies: List[str], role_level: int) -> Dict:
        """Create a new role"""
        endpoint = "/v1/admin/role"
        data = {
            "role_name": role_name,
            "policies": policies,
            "role_level": role_level
        }
        
        return self.api_client.post(endpoint, json=data)

    def update_role(self, role_name: str, operation: str, policies: List[str], role_level: Optional[int] = None) -> Dict:
        """Update an existing role"""
        endpoint = "/v1/admin/role"
        params = {
            "role_name": role_name,
            "operation": operation
        }
        
        data = {
            "policies": policies
        }
        
        if role_level is not None:
            data["role_level"] = role_level
            
        return self.api_client.put(endpoint, params=params, json=data)

    def get_role(self, role_name: Optional[str] = None) -> Dict:
        """Get role information"""
        endpoint = "/v1/admin/role"
        params = {}
        
        if role_name:
            params["role_name"] = role_name
            
        return self.api_client.get(endpoint, params=params)

    def delete_role(self, role_name: str) -> Dict:
        """Delete a role"""
        endpoint = "/v1/admin/role"
        params = {
            "role_name": role_name
        }
            
        return self.api_client.delete(endpoint, params=params)

    # RBAC Deployment Settings Operations
    def get_deployment_settings(self, service: str = "rbac", platform: Optional[str] = None,
                               package_name: Optional[str] = None, is_email_user_pool: Optional[bool] = None) -> Dict:
        """Get deployment settings for a service
        
        Args:
            service: Service whose configuration is to be fetched (default: rbac)
            platform: Platform (ios/android) - required if service is mobile_app
            package_name: Package name - required if service is mobile_app
            is_email_user_pool: Use true for older/email-only userPool or false for newer/email-and-phone userPool
        """
        endpoint = f"/v1/admin/deployment_settings/{service}"
        params = {}
        
        if platform:
            params["platform"] = platform
        if package_name:
            params["package_name"] = package_name
        if is_email_user_pool is not None:
            params["isEmailUserPool"] = str(is_email_user_pool).lower()
            
        return self.api_client.get(endpoint, params=params)

    def update_deployment_settings(self, service: str = "rbac", **kwargs) -> Dict:
        """Update deployment settings for a service
        
        Args:
            service: Service to configure (default: rbac)
            **kwargs: Service-specific configuration parameters
        """
        endpoint = f"/v1/admin/deployment_settings/config/{service}"
        data = {}
        
        # Handle different services based on documentation
        if service == "rbac" and "rbac_enabled" in kwargs:
            data["rbac_enabled"] = kwargs["rbac_enabled"]
        elif service == "node_apis" and "node_apis_enabled" in kwargs:
            data["node_apis_enabled"] = kwargs["node_apis_enabled"]
        elif service == "custom_user_context" and "custom_user_context_enabled" in kwargs:
            data["custom_user_context_enabled"] = kwargs["custom_user_context_enabled"]
        elif service == "location_trigger" and "location_trigger_config" in kwargs:
            data.update(kwargs["location_trigger_config"])
        elif service == "encryption" and "encryption_enabled" in kwargs:
            data["encryption_enabled"] = kwargs["encryption_enabled"]
        elif service == "user_archival" and "user_archival_enabled" in kwargs:
            data["user_archival_enabled"] = kwargs["user_archival_enabled"]
        elif service == "oauth_only" and "oauth_only_enabled" in kwargs:
            data["oauth_only_enabled"] = kwargs["oauth_only_enabled"]
        elif service == "cmd_resp_history" and "cmd_resp_history_enabled" in kwargs:
            data["cmd_resp_history_enabled"] = kwargs["cmd_resp_history_enabled"]
        elif service == "custom_sms" and "custom_sms_config" in kwargs:
            data.update(kwargs["custom_sms_config"])
        elif service == "node_data_access" and "node_data_access_config" in kwargs:
            data.update(kwargs["node_data_access_config"])
        elif service == "ota_network_serialisation_degree" and "ota_network_serialisation_degree" in kwargs:
            data["ota_network_serialisation_degree"] = kwargs["ota_network_serialisation_degree"]
            
        return self.api_client.put(endpoint, json=data)
