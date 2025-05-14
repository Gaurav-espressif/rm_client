from typing import Dict, Optional, Union, List
from ..utils.api_client import ApiClient


class OTAService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def upload_image(
            self,
            base64_fwimage: str,
            image_name: str,
            fw_version: Optional[str] = None,
            model: Optional[str] = None,
            type: Optional[str] = None,
            **kwargs
    ) -> Dict:
        """Upload a new firmware image with debug information"""
        endpoint = "/v1/admin/otaimage"

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

        # Debug prints


        # Get token information
        try:
            token_data = self.api_client.token_store.get_token()

        except Exception as token_error:
            print(f"\nToken debug error: {str(token_error)}")



        try:
            print("\nSending request...")
            response = self.api_client.post(endpoint, json=payload)
            return response

        except Exception as e:
            print("\n=== ERROR DETAILS ===")
            print(f"Error Message: {str(e)}")

            if hasattr(e, 'response'):
                # Additional debug for AWS API Gateway errors
                if 'x-amzn-errortype' in e.response.headers:
                    print(f"AWS Error Type: {e.response.headers['x-amzn-errortype']}")

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