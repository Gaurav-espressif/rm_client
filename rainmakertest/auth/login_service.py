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

        try:
            # Make the login request without authentication
            response = self.api_client.post(endpoint, data=payload, authenticate=False)

            # If API returned failure response directly
            if response.get("status") == "failure":
                return response

            # Check for successful response structure
            if not isinstance(response.get("data"), dict):
                return {
                    "status": "failure",
                    "description": "Invalid login response format",
                    "error_code": 400
                }

            response_data = response["data"]

            # Verify we have the required access token
            if not response_data.get("accesstoken"):
                return {
                    "status": "failure",
                    "description": "Login failed - no access token in response",
                    "error_code": 401
                }

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
                return {
                    "status": "failure",
                    "description": f"Failed to save tokens: {str(e)}",
                    "error_code": 500
                }

            # Return success response
            return {
                "status": "success",
                "description": "Login successful",
                "token": {
                    "access_token": token_data["access_token"],
                    "id_token": token_data.get("id_token", ""),
                    "refresh_token": token_data.get("refresh_token", "")
                }
            }

        except Exception as e:
            return {
                "status": "failure",
                "description": str(e),
                "error_code": 500
            }

    def logout_user(self, refresh_token: Optional[str] = None) -> Dict:
        """Logout current user"""
        endpoint = "/v1/logout2"
        payload = {}
        if refresh_token:
            payload["refresh_token"] = refresh_token

        try:
            response = self.api_client.post(endpoint, data=payload)
            self.api_client.clear_token()
            return response
        except Exception as e:
            return {
                "status": "failure",
                "description": str(e),
                "error_code": 500
            }