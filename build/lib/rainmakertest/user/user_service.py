from typing import Dict, Optional
from ..utils.api_client import ApiClient


class UserService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create_user(self, user_name: str, password: str, locale: str = "no_locale") -> Dict:
        """Create a new user account"""
        endpoint = "/v1/user"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": user_name,
            "password": password
        }
        print(f"Creating user with payload: {payload}")
        # Add authenticate=False to disable token requirement
        return self.api_client.post(endpoint, data=payload, params=params, authenticate=False)

    def confirm_user(self, username: str, verification_code: str, locale: str = "no_locale") -> Dict:
        """Confirm user account with verification code"""
        endpoint = "/v1/user"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": username,
            "verification_code": verification_code
        }
        # Add authenticate=False to disable token requirement
        return self.api_client.post(endpoint, data=payload, params=params, authenticate=False)

    def get_user_info(self) -> Dict:
        """Get current user's information using access token"""
        endpoint = "/v1/user"
        # The API client now handles exceptions and returns a structured dict for errors
        response = self.api_client.get(endpoint)

        # If the API client returned an error dict, return it directly
        if isinstance(response, dict) and response.get("status") == "failure":
            return response

        # Original validation logic for successful responses
        if not response:
            return {"status": "failure", "description": "Empty response from server", "error_code": 0} # Custom error
        if not isinstance(response, dict):
            return {"status": "failure", "description": "Invalid response format - expected dictionary", "error_code": 0} # Custom error
        if "user_id" not in response:
            return {"status": "failure", "description": "Response missing required field: user_id", "error_code": 0} # Custom error

        return {
            "user_id": response["user_id"],
            "user_name": response.get("user_name", ""),
            "locale": response.get("locale", "no_locale"),
            "super_admin": response.get("super_admin", False),
            "admin": response.get("admin", False),
            "mfa": response.get("mfa", False),
            **{k: v for k, v in response.items()
               if k not in ["user_id", "user_name", "locale", "super_admin", "admin", "mfa"]}
        }

    def update_user(self, name: Optional[str] = None, phone_number: Optional[str] = None) -> Dict:
        """Update user information"""
        endpoint = "/v1/user"
        payload = {}
        if name:
            payload["name"] = name
        if phone_number:
            payload["phone_number"] = phone_number

        return self.api_client.put(endpoint, data=payload)

    def delete_user(self, verification_code: Optional[str] = None, request: bool = False) -> Dict:
        """Delete user account"""
        endpoint = "/v1/user"
        params = {}
        if verification_code:
            params["verification_code"] = verification_code
        if request:
            params["request"] = "true"

        return self.api_client.delete(endpoint, params=params)