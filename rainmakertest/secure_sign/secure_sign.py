from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class SecureSignService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def create_secure_sign(self, ota_image_id: str, key_names: List[str],
                          sign_boot_loader: bool = False) -> Dict:
        """Create a secure signing request for OTA images
        
        Args:
            ota_image_id: ID of the OTA image to sign
            key_names: List of key names to use for signing
            sign_boot_loader: Whether to sign the bootloader as well
        """
        endpoint = "/v1/admin/secure_sign"
        data = {
            "ota_image_id": ota_image_id,
            "key_names": key_names,
            "sign_boot_loader": sign_boot_loader
        }
        
        return self.api_client.post(endpoint, json=data)

    def get_secure_sign_status(self, request_id: str) -> Dict:
        """Get the status of a secure signing request
        
        Args:
            request_id: ID of the signing request
        """
        endpoint = "/v1/admin/secure_sign"
        params = {"request_id": request_id}
        return self.api_client.get(endpoint, params=params)

    def get_signed_images(self, key_name: Optional[str] = None,
                         num_records: Optional[int] = None,
                         start_id: Optional[str] = None) -> Dict:
        """Get images signed by a specific key
        
        Args:
            key_name: Name of the key to filter by
            num_records: Number of records to fetch
            start_id: Start ID for pagination
        """
        endpoint = "/v1/admin/secure_sign/signed_images"
        params = {}
        
        if key_name:
            params["key_name"] = key_name
        if num_records:
            params["num_records"] = num_records
        if start_id:
            params["start_id"] = start_id
            
        return self.api_client.get(endpoint, params=params)

    def get_signing_keys(self, image_id: str,
                        num_records: Optional[int] = None,
                        start_id: Optional[str] = None) -> Dict:
        """Get the keys used to sign a specific image
        
        Args:
            image_id: ID of the image to get signing keys for
            num_records: Number of records to fetch
            start_id: Start ID for pagination
        """
        endpoint = "/v1/admin/secure_sign/signing_keys"
        params = {"image_id": image_id}
        
        if num_records:
            params["num_records"] = num_records
        if start_id:
            params["start_id"] = start_id
            
        return self.api_client.get(endpoint, params=params)
