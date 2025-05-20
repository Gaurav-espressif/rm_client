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

        # Make the login request without authentication
        response = self.api_client.post(endpoint, data=payload, authenticate=False)
        #gaurav
        # Check if the response indicates failure
        if response.get("status") == "failure":
            error_msg = response.get("description", "Login failed")
            raise ValueError(error_msg)

        # Check for successful response structure
        if not isinstance(response.get("data"), dict):
            raise ValueError("Invalid login response format")

        response_data = response["data"]

        # Verify we have the required access token
        if not response_data.get("accesstoken"):
            raise ValueError("Login failed - no access token in response")

        # Prepare token data
        token_data = {
            "access_token": response_data["accesstoken"],
            "id_token": response_data.get("idtoken", ""),
            "refresh_token": response_data.get("refreshtoken", "")
        }

        # Store the tokens
        try:
            self.api_client.set_access_token(
                token_data["access_token"],
                token_data.get("id_token")
            )
            # Store refresh token if available
            if token_data.get("refresh_token"):
                self.api_client.token_store.save_token({
                    "refresh_token": token_data["refresh_token"]
                })
        except Exception as e:
            raise RuntimeError(f"Failed to save tokens: {str(e)}")

        # Return the expected response structure
        return {
            "status": "success",
            "description": "Login successful",
            "token": {
                "access_token": token_data["access_token"],
                "id_token": token_data.get("id_token", ""),
                "refresh_token": token_data.get("refresh_token", "")
            }
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