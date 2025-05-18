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
        # Add authenticate=False to disable token requirement
        return self.api_client.post(endpoint, data=payload, params=params, authenticate=False)

    def confirm_user(self, username: str, verification_code: str, locale: str = "no_locale") -> Dict:
        """Confirm user account with verification code"""
        endpoint = "/v1/user2"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": username,
            "verification_code": verification_code
        }
        # Add authenticate=False to disable token requirement
        return self.api_client.post(endpoint, data=payload, params=params, authenticate=False)

    def get_user_info(self) -> Dict:
        """Get current user's information using access token"""
        endpoint = "/v1/user2"
        try:
            # Verify we have a valid token first
            token_data = self.api_client.token_store.get_token()
            if not token_data or not token_data.get("access_token"):
                raise ValueError("No valid access token available - please login first")

            # Make the API call (token should be auto-added by api_client)
            response = self.api_client.get(endpoint)

            if not response:
                raise ValueError("Empty response from server")

            # Only enforce absolutely required fields
            if not isinstance(response, dict):
                raise ValueError("Invalid response format - expected dictionary")

            # Minimal required fields (just user_id)
            if "user_id" not in response:
                raise ValueError("Response missing required field: user_id")

            # Set sensible defaults for optional fields
            return {
                "user_id": response["user_id"],
                "user_name": response.get("user_name", ""),
                "locale": response.get("locale", "no_locale"),
                "super_admin": response.get("super_admin", False),
                "admin": response.get("admin", False),
                "mfa": response.get("mfa", False),
                # Include any additional fields present in response
                **{k: v for k, v in response.items()
                   if k not in ["user_id", "user_name", "locale", "super_admin", "admin", "mfa"]}
            }

        except Exception as e:
            print(f"\nUSER INFO ERROR DETAILS:")
            print(f"Endpoint: {endpoint}")
            print(f"Token Present: {'Yes' if token_data else 'No'}")
            if token_data:
                print(f"Token: {token_data.get('access_token', '')[:10]}...")
            print(f"Response: {response if 'response' in locals() else 'Not available'}")
            raise Exception(f"Failed to get user info: {str(e)}") from e

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