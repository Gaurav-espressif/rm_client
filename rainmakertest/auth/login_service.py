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
                return {
                    "status": "failure",
                    "message": response.get("description", "Login failed"),
                    "error_code": response.get("error_code", 401)
                }

            # Check if we got a proper response with access token
            if not isinstance(response.get("data"), dict) or not response["data"].get("accesstoken"):
                return {
                    "status": "failure",
                    "message": "Invalid login response from server",
                    "error_code": 500
                }

            response_data = response["data"]
            token_data = {
                "access_token": response_data["accesstoken"],
                "id_token": response_data.get("idtoken", ""),
                "refresh_token": response_data.get("refreshtoken", "")
            }

            # Store the tokens
            self.api_client.set_access_token(
                token_data["access_token"],
                token_data.get("id_token")
            )
            if token_data.get("refresh_token"):
                self.api_client.token_store.save_token({
                    "refresh_token": token_data["refresh_token"]
                })

            # Return the exact structure the CLI expects
            return {
                "status": "success",
                "token": token_data,
                "message": "Login successful"
            }

        except Exception as e:
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
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