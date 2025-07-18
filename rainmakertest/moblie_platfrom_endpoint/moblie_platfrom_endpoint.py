from typing import Dict, Optional
from ..utils.api_client import ApiClient
import logging

class MobilePlatformEndpointService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def create_platform_endpoint(self, platform: str, mobile_device_token: str, platform_type: str) -> Dict:
        """Create a new platform endpoint for mobile device"""
        endpoint = "/v1/user/push_notification/mobile_platform_endpoint"
        data = {
            "platform": platform,
            "mobile_device_token": mobile_device_token,
            "platform_type": platform_type
        }
        
        return self.api_client.post(endpoint, json=data)

    def get_platform_endpoints(self) -> Dict:
        """Get configured platform endpoints"""
        endpoint = "/v1/user/push_notification/mobile_platform_endpoint"
        return self.api_client.get(endpoint)

    def delete_platform_endpoint(self, mobile_device_token: Optional[str] = None, endpoint: Optional[str] = None) -> Dict:
        """Delete a configured platform endpoint"""
        if not mobile_device_token and not endpoint:
            raise ValueError("Either mobile_device_token or endpoint must be specified")
            
        endpoint_url = "/v1/user/push_notification/mobile_platform_endpoint"
        params = {}
        
        if mobile_device_token:
            params["mobile_device_token"] = mobile_device_token
        if endpoint:
            params["endpoint"] = endpoint
            
        return self.api_client.delete(endpoint_url, params=params)
