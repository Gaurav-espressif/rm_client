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
            # Re-raising for specific file errors is fine here if you want distinct error handling
            raise ValueError(f"Error reading file {file_path}: {str(e)}") from e


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
                print(f"\nNo firmware provided. Using default file: {self.default_bin_path}")
                base64_fwimage = self._file_to_base64(self.default_bin_path)
            else:
                raise ValueError("No firmware provided (use --base64, --file, or ensure switch.bin exists)")


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

        # The API client will handle exceptions and return a structured dict
        return self.api_client.post(endpoint, json=payload)


    def get_images(
            self,
            ota_image_id: Optional[str] = None,
            ota_image_name: Optional[str] = None,
            type: Optional[str] = None,
            model: Optional[str] = None,
            num_records: Optional[str] = None,
            start_id: Optional[str] = None,
            contains: bool = False,
            archived: bool = False,
            all: bool = False
    ) -> Dict:
        """Get OTA image details"""
        endpoint = "/v1/admin/otaimage"
        params = {}
        if ota_image_id:
            params["ota_image_id"] = ota_image_id
        if ota_image_name:
            params["image_name"] = ota_image_name
        if type:
            params["type"] = type
        if model:
            params["model"] = model
        if num_records:
            params["num_records"] = num_records
        if start_id:
            params["start_id"] = start_id
        if contains:
            params["contains"] = "true"
        if archived:
            params["archived"] = "true"
        if all:
            params["all"] = "true"

        # Get the raw response from the API
        response = self.api_client.get(endpoint, params=params)
        
        # If we get a single image (when using ota_image_id), wrap it in a list
        if response and isinstance(response, dict) and 'ota_image_id' in response:
            return {'ota_images': [response]}
        
        # If we get a list of images, return as is
        if response and isinstance(response, list):
            return {'ota_images': response}
            
        return {'ota_images': []} if response is None else response

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


    def get_package_upload_url(self, file_name: str) -> Dict:
        """Get pre-signed URL for firmware package upload.
        
        This API fetches a presigned URL that can be used to upload the firmware package.
        The file_name must include the file extension.
        
        Args:
            file_name: Name of the file with file extension to upload
            
        Returns:
            Dict containing the pre-signed URL for upload
        """
        endpoint = "/v1/admin/otaimage/package/upload"
        params = {"file_name": file_name}
        return self.api_client.get(endpoint, params=params)

    def upload_package(self, image_name: str, type: str, file_path: str) -> Dict:
        """Upload a new firmware package.
        
        This API uploads a new package containing the Firmware image to Rainmaker Cloud.
        
        Args:
            image_name: Name of the image (e.g. "Alexa echo 2")
            type: Type of the image (e.g. "alexa")
            file_path: Path to the file that has been uploaded to S3
            
        Returns:
            Dict containing the upload response
        """
        endpoint = "/v1/admin/otaimage/package"
        payload = {
            "image_name": image_name,
            "type": type,
            "file_path": file_path
        }
        return self.api_client.post(endpoint, json=payload)