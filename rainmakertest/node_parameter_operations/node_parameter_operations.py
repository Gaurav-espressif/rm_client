from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class NodeParameterOperationsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def update_node_params(self, params_list: List[Dict], node_id: Optional[str] = None) -> Dict:
        """Update node parameters
        
        Args:
            params_list: List of dictionaries containing node_id and payload
            node_id: Optional node_id for single node update via query parameter
        """
        endpoint = "/v1/user/nodes/params"
        
        # If using query parameter for single node
        if node_id:
            params = {"node_id": node_id}
            if len(params_list) == 1 and "payload" in params_list[0]:
                return self.api_client.put(endpoint, params=params, json=params_list)
            else:
                raise ValueError("When using node_id as query parameter, exactly one payload is required")
        
        # For multiple nodes, send all updates in a single request
        else:
            # Validate each item has node_id and payload
            for item in params_list:
                if "node_id" not in item:
                    raise ValueError("node_id is required in each item when not using query parameter")
                if "payload" not in item:
                    raise ValueError("payload is required in each item")
            
            # Send all updates in a single request
            return self.api_client.put(endpoint, json=params_list)

    def get_node_params(self, node_id: str) -> Dict:
        """Get node parameters
        
        Args:
            node_id: ID of the node to get parameters for
        """
        endpoint = "/v1/user/nodes/params"
        params = {"node_id": node_id}
        return self.api_client.get(endpoint, params=params)
