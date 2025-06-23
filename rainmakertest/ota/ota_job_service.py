from rainmakertest.utils.api_client import ApiClient
from typing import Dict, Optional, List, Union
from datetime import datetime


class OTAJobService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create_job(
            self,
            ota_job_name: str,
            ota_image_id: str,
            description: Optional[str] = None,
            nodes: Optional[List[str]] = None,
            priority: int = 5,
            timeout: int = 1296000,
            force_push: bool = True,
            user_approval: bool = False,
            notify: bool = False,
            continuous: bool = False,
            network_serialised: bool = False,
    ) -> Dict:
        """Create a new OTA job"""
        endpoint = "/v1/admin/otajob"
        params = {
            "force_push": "true",
            "user_approval": "true" if user_approval else "false",
            "notify": "true" if notify else "false",
            "continuous": "true" if continuous else "false",
            "network_serialised": "true" if network_serialised else "false"
        }

        payload = {
            "ota_job_name": ota_job_name,
            "description": description or "Default OTA job description.",
            "priority": priority,
            "timeout": timeout,
            "ota_image_id": ota_image_id
        }

        if nodes:
            # Ensure nodes is a list (split string if needed)
            if isinstance(nodes, str):
                payload["nodes"] = [nodes]  # Create single-item list from string
            else:
                payload["nodes"] = nodes

        return self.api_client.post(endpoint, json=payload, params=params)

    def get_jobs(
            self,
            ota_job_id: Optional[str] = None,
            ota_job_name: Optional[str] = None,
            ota_image_id: Optional[str] = None,
            archived: Optional[bool] = None,
            all: bool = False
    ) -> Dict:
        """Get OTA job details"""
        endpoint = "/v1/admin/otajob"
        params = {}
        if ota_job_id:
            params["ota_job_id"] = ota_job_id
        if ota_job_name:
            params["ota_job_name"] = ota_job_name
        if ota_image_id:
            params["ota_image_id"] = ota_image_id
        if archived is not None:
            params["archived"] = "true" if archived else "false"
        if all:
            params["all"] = "true"

        return self.api_client.get(endpoint, params=params)

    def get_job_status(self, ota_job_id: str) -> Dict:
        """
        Get the status of an OTA job including latest OTA status for nodes

        Args:
            ota_job_id: The ID of the OTA job to check status for

        Returns:
            Dictionary containing the OTA job status information
        """
        endpoint = f"/v1/admin/otajob/status"
        params = {
            "ota_job_id": ota_job_id
        }
        return self.api_client.get(endpoint, params=params)

    def update_job(
            self,
            ota_job_id: str,
            archive: Optional[bool] = None
    ) -> Dict:
        """
        Cancel or archive an OTA job

        Args:
            ota_job_id: The ID of the OTA job to update
            archive: If None/False, cancel the job. If True, archive the job.

        Returns:
            Dictionary containing the API response
        """
        endpoint = "/v1/admin/otajob"
        payload = {
            "ota_job_id": ota_job_id
        }

        # Only add archive flag if explicitly True
        if archive:
            payload["archive"] = True

        # The API client will handle exceptions and return a structured dict
        return self.api_client.put(endpoint, json=payload)