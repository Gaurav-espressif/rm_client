from typing import Dict, Optional
from ..utils.api_client import ApiClient

class LoginService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def login_user(self, user_name: str, password: str) -> Dict:
        """Login with username and password"""
        endpoint = "/v1/login2"
        payload = {
            "user_name": user_name,
            "password": password
        }
        response = self.api_client.post(endpoint, data=payload, authenticate=False) # Don't authenticate login request

        # Enhanced validation
        if not response.get("accesstoken"):
            error_msg = response.get("description", "Login failed - no access token in response")
            raise ValueError(error_msg)

        # Standardized token storage
        token_data = {
            "access_token": response["accesstoken"],
            "id_token": response.get("idtoken", ""),
            "refresh_token": response.get("refreshtoken", "")
        }

        try:
            self.api_client.set_access_token(token_data["access_token"], token_data.get("id_token"))
        except Exception as e:
            raise RuntimeError(f"Failed to save tokens: {str(e)}")

        # Return enriched response
        return {
            "status": "success",
            "description": "Login successful",
            "token": token_data  # This matches what the CLI expects
        }

    def logout_user(self, refresh_token: Optional[str] = None) -> Dict:
        """Logout current user"""
        endpoint = "/v1/logout2"
        payload = {}
        if refresh_token:
            payload["refresh_token"] = refresh_token

        response = self.api_client.post(endpoint, data=payload)
        self.api_client.clear_token()
        return response