from typing import Dict, List, Optional
from ..utils.api_client import ApiClient


class NodeAdminService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_admin_nodes(
            self,
            node_id: Optional[str] = None,
            node_type: Optional[str] = None,
            model: Optional[str] = None,
            fw_version: Optional[str] = None,
            subtype: Optional[str] = None,
            project_name: Optional[str] = None,
            status: Optional[str] = None,
            num_records: Optional[int] = None,
            start_id: Optional[str] = None
    ) -> List[Dict]:
        """Get nodes claimed by admin with filtering options"""
        endpoint = "/v1/admin/nodes"
        params = {}
        if node_id:
            params["node_id"] = node_id
        if node_type:
            params["type"] = node_type
        if model:
            params["model"] = model
        if fw_version:
            params["fw_version"] = fw_version
        if subtype:
            params["subtype"] = subtype
        if project_name:
            params["project_name"] = project_name
        if status:
            params["status"] = status
        if num_records:
            params["num_records"] = num_records
        if start_id:
            params["start_id"] = start_id

        return self.api_client.get(endpoint, params=params)