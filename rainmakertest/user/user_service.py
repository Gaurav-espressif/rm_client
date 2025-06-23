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
        return self.api_client.post(endpoint, data=payload, authenticate=False)

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
        endpoint = "/v1/user"
        return self.api_client.get(endpoint)

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
    def change_password(self, current_password: str, new_password: str) -> Dict:
        """Change user password"""
        endpoint = "/v1/password2"
        payload = {
            "password": current_password,
            "newpassword": new_password
        }
        return self.api_client.put(endpoint, json=payload)

    def forgot_password(self, user_name: str, password: Optional[str] = None, 
                       verification_code: Optional[str] = None, locale: str = "empty") -> Dict:
        """Handle forgot password request"""
        endpoint = "/v1/forgotpassword2"
        params = {"locale": locale} if locale != "empty" else None
        
        if password and verification_code:
            # Confirm forgot password with new password and verification code
            payload = {
                "user_name": user_name,
                "password": password,
                "verification_code": verification_code
            }
        else:
            # Request forgot password - send verification code
            payload = {
                "user_name": user_name
            }
        
        return self.api_client.put(endpoint, json=payload, params=params, authenticate=False)

    def update_user_details(self, name: Optional[str] = None, phone_number: Optional[str] = None,
                           verification_code: Optional[str] = None, mfa: Optional[bool] = None,
                           locale: Optional[str] = None) -> Dict:
        """Update user details including name, phone number, MFA status, and locale"""
        endpoint = "/v1/user2"
        payload = {}
        
        if name is not None:
            payload["name"] = name
        if phone_number is not None:
            payload["phone_number"] = phone_number
        if verification_code is not None:
            payload["verification_code"] = verification_code
        if mfa is not None:
            payload["mfa"] = mfa
        if locale is not None:
            payload["locale"] = locale
            
        return self.api_client.put(endpoint, json=payload)
