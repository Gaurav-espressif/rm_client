import base64
import os
from typing import Dict, Optional, Union, List
from ..utils.api_client import ApiClient


class OTAService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        # Set default bin file path (adjust as needed)
        self.default_bin_path = os.path.join(os.path.dirname(__file__), 'switch.bin')

    def _file_to_base64(self, file_path: str) -> str:
        """Convert a binary file to base64 string"""
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                return base64.b64encode(file_content).decode('utf-8')
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            raise

    def upload_image(
            self,
            image_name: str,
            fw_version: Optional[str] = None,
            model: Optional[str] = None,
            type: Optional[str] = None,
            base64_fwimage: Optional[str] = None,
            bin_file_path: Optional[str] = None,
            **kwargs
    ) -> Dict:
        """Upload a new firmware image (supports base64, file path, or default file)"""
        endpoint = "/v1/admin/otaimage"

        # Handle firmware input (priority: bin_file > base64 > default file)
        if bin_file_path:
            base64_fwimage = self._file_to_base64(bin_file_path)
        elif not base64_fwimage:
            if os.path.exists(self.default_bin_path):
                print(f"\n⚠No firmware provided. Using default file: {self.default_bin_path}")
                base64_fwimage = self._file_to_base64(self.default_bin_path)
            else:
                raise ValueError(
                    "No firmware provided (use --base64, --file, or ensure switch.bin exists)"
                )

        # Prepare payload
        payload = {
            "fw_version": fw_version or "1.0.0",
            "image_name": image_name,
            "model": model or "ESP32",
            "type": type or "development",
            "base64_fwimage": base64_fwimage
        }
        payload.update(kwargs)
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = self.api_client.post(endpoint, json=payload)
            return response
        except Exception as e:
            print(f"\nUpload failed: {str(e)}")
            raise

    def get_images(
            self,
            ota_image_id: Optional[str] = None,
            ota_image_name: Optional[str] = None,
            contains: bool = False
    ) -> Dict:
        """Get OTA image details"""
        endpoint = "/v1/admin/otaimage"
        params = {}
        if ota_image_id:
            params["ota_image_id"] = ota_image_id
        if ota_image_name:
            params["ota_image_name"] = ota_image_name
        if contains:
            params["contains"] = "true"

        return self.api_client.get(endpoint, params=params)

    def delete_image(self, ota_image_id: str) -> Dict:
        """Delete an OTA image"""
        endpoint = "/v1/admin/otaimage"
        params = {"ota_image_id": ota_image_id}
        return self.api_client.delete(endpoint, params=params)

    def archive_image(
            self,
            ota_image_id: str,
            archive: bool = True
    ) -> Dict:
        """Archive or unarchive an OTA image"""
        endpoint = "/v1/admin/otaimage"
        params = {
            "ota_image_id": ota_image_id,
            "archive": "true" if archive else "false"
        }
        return self.api_client.put(endpoint, params=params)