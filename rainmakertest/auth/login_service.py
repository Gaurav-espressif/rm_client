from typing import Dict
import logging

import jwt

from ..utils.api_client import ApiClient

class LoginService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def login_user(self, user_name: str, password: str) -> Dict:
        """Login with username and password"""
        endpoint = "/v1/login2"
        payload = {
            "user_name": user_name,
            "password": password
        }

        try:
            # Make the login request without authentication
            response = self.api_client.post(endpoint, json=payload, authenticate=False)
            self.logger.debug(f"Login response: {response}")

            if response.get("status") != "success":
                return {
                    "status": "failure",
                    "message": response.get("description", "Login failed"),
                    "error_code": response.get("error_code", 401)
                }

            response_data = response.get("data", {})
            if not isinstance(response_data, dict):
                return {
                    "status": "failure",
                    "message": "Invalid response format from server",
                    "error_code": 500
                }

            # Verify required fields in response
            required_fields = ["accesstoken", "idtoken"]
            if not all(field in response_data for field in required_fields):
                return {
                    "status": "failure",
                    "message": "Missing required token fields in response",
                    "error_code": 500
                }

            # Store the tokens
            token_data = {
                "access_token": response_data["accesstoken"],
                "id_token": response_data["idtoken"],
                "refresh_token": response_data.get("refreshtoken", "")
            }
            self.api_client.set_access_token(
                token_data["access_token"],
                token_data["id_token"]
            )

            # Verify the token contains required claims
            try:
                decoded = jwt.decode(token_data["access_token"], options={"verify_signature": False})
                if not decoded.get("sub"):
                    return {
                        "status": "failure",
                        "message": "Token missing required user claims",
                        "error_code": 401
                    }
            except Exception as e:
                return {
                    "status": "failure",
                    "message": f"Token validation failed: {str(e)}",
                    "error_code": 401
                }

            return {
                "status": "success",
                "message": "Login successful",
                "token": token_data
            }

        except Exception as e:
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }


    class LogoutService:
        def __init__(self, api_client: ApiClient):
            self.api_client = api_client

        def logout(self) -> Dict:
            """Perform logout operations"""
            try:
                # Clear client-side tokens
                self.api_client.clear_token()

                # Optional: Make server-side logout request
                response = self.api_client.post('/v1/logout', authenticate=True)

                return {
                    'status': 'success',
                    'message': 'Successfully logged out',
                    'server_response': response
                }
            except Exception as e:
                return {
                    'status': 'failure',
                    'message': str(e),
                    'error_code': 500
                }