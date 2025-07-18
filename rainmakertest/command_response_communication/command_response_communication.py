from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class CommandResponseCommunicationService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    # Admin Command Response Operations
    def create_admin_command_response(self, node_ids: List[str], cmd: int,
                                    data: Dict, is_base64: bool = False,
                                    timeout: Optional[int] = None,
                                    override: Optional[bool] = None) -> Dict:
        """Create a new command response request as admin"""
        endpoint = "/v1/admin/nodes/cmd"
        payload = {
            "node_ids": node_ids,
            "cmd": cmd,
            "data": data,
            "is_base64": is_base64
        }
        
        if timeout is not None:
            payload["timeout"] = timeout
        if override is not None:
            payload["override"] = override
            
        return self.api_client.post(endpoint, json=payload)

    def get_admin_command_response(self, request_id: Optional[str] = None,
                                 node_id: Optional[str] = None,
                                 status: Optional[str] = None,
                                 start_time: Optional[int] = None,
                                 end_time: Optional[int] = None,
                                 cmd_id: Optional[int] = None,
                                 desc_order: bool = True,
                                 start_id: Optional[str] = None,
                                 num_records: int = 10) -> Dict:
        """Get command response requests as admin"""
        endpoint = "/v1/admin/nodes/cmd"
        params = {
            "desc_order": desc_order,
            "num_records": num_records
        }
        
        # Add optional query parameters
        if request_id:
            params["request_id"] = request_id
        if node_id:
            params["node_id"] = node_id
        if status:
            params["status"] = status
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if cmd_id:
            params["cmd_id"] = cmd_id
        if start_id:
            params["start_id"] = start_id
            
        return self.api_client.get(endpoint, params=params)

    # User Command Response Operations
    def create_user_command_response(self, node_ids: List[str], cmd: int,
                                   data: Dict, is_base64: bool = False,
                                   timeout: Optional[int] = None,
                                   override: Optional[bool] = None) -> Dict:
        """Create a new command response request as user"""
        endpoint = "/v1/user/nodes/cmd"
        payload = {
            "node_ids": node_ids,
            "cmd": cmd,
            "data": data,
            "is_base64": is_base64
        }
        
        if timeout is not None:
            payload["timeout"] = timeout
        if override is not None:
            payload["override"] = override
            
        return self.api_client.post(endpoint, json=payload)

    def get_user_command_response(self, request_id: Optional[str] = None,
                                node_id: Optional[str] = None,
                                status: Optional[str] = None,
                                start_time: Optional[int] = None,
                                end_time: Optional[int] = None,
                                cmd_id: Optional[int] = None,
                                desc_order: bool = True,
                                start_id: Optional[str] = None,
                                num_records: int = 10) -> Dict:
        """Get command response requests as user"""
        endpoint = "/v1/user/nodes/cmd"
        params = {
            "desc_order": desc_order,
            "num_records": num_records
        }
        
        # Add optional query parameters
        if request_id:
            params["request_id"] = request_id
        if node_id:
            params["node_id"] = node_id
        if status:
            params["status"] = status
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if cmd_id:
            params["cmd_id"] = cmd_id
        if start_id:
            params["start_id"] = start_id
            
        return self.api_client.get(endpoint, params=params)
