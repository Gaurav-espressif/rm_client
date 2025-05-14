from typing import Dict, Optional
from ..utils.api_client import ApiClient


class UserService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create_user(self, user_name: str, password: str, locale: str = "no_locale") -> Dict:
        """Create a new user account"""
        endpoint = "/v1/user2"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": user_name,
            "password": password
        }
        print(f"Creating user with payload: {payload}")
        return self.api_client.post(endpoint, data=payload, params=params)

    def confirm_user(self, username: str, verification_code: str, locale: str = "no_locale") -> Dict:
        """Confirm user account with verification code"""
        endpoint = "/v1/user2"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": username,
            "verification_code": verification_code
        }
        return self.api_client.post(endpoint, data=payload, params=params)

    def get_user_info(self) -> Dict:
        """Get current user's information"""
        endpoint = "/v1/user2"
        try:
            response = self.api_client.get(endpoint)
            if not response:
                raise ValueError("Empty response from server")

            # Basic response validation
            required_fields = {"user_id", "user_name", "locale"}
            if not all(field in response for field in required_fields):
                missing = required_fields - response.keys()
                raise ValueError(f"Missing required fields: {missing}")

            return response
        except Exception as e:
            print(f"\nUSER INFO ERROR DETAILS:")
            print(f"Endpoint: {endpoint}")
            token_data = self.api_client.token_store.get_token()
            access_token = token_data.get("access_token", "") if token_data else ""
            print(f"Token: {access_token[:10]}...")
            raise Exception(f"Failed to get user info: {str(e)}")

    def update_user(self, name: Optional[str] = None, phone_number: Optional[str] = None) -> Dict:
        """Update user information"""
        endpoint = "/v1/user2"
        payload = {}
        if name:
            payload["name"] = name
        if phone_number:
            payload["phone_number"] = phone_number

        return self.api_client.put(endpoint, data=payload)

    def delete_user(self, verification_code: Optional[str] = None, request: bool = False) -> Dict:
        """Delete user account"""
        endpoint = "/v1/user2"
        params = {}
        if verification_code:
            params["verification_code"] = verification_code
        if request:
            params["request"] = "true"

        return self.api_client.delete(endpoint, params=params)