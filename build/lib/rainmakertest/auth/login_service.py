from typing import Dict
import logging
import json

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

            # Check if response is a string (JSON string)
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError:
                    return {
                        "status": "failure",
                        "message": "Invalid JSON response from server",
                        "error_code": 500
                    }

            # Handle direct token response
            if "accesstoken" in response:
                token_data = {
                    "access_token": response["accesstoken"],
                    "id_token": response.get("idtoken", ""),
                    "refresh_token": response.get("refreshtoken", "")
                }
            # Handle nested data response
            elif "data" in response and isinstance(response["data"], dict):
                response_data = response["data"]
                token_data = {
                    "access_token": response_data.get("accesstoken", ""),
                    "id_token": response_data.get("idtoken", ""),
                    "refresh_token": response_data.get("refreshtoken", "")
                }
            else:
                return {
                    "status": "failure",
                    "message": f"Unexpected response format: {response}",
                    "error_code": 500
                }

            # Verify we have the required tokens
            if not token_data["access_token"]:
                return {
                    "status": "failure",
                    "message": "No access token in response",
                    "error_code": 401
                }

            # Store the access token in the API client and config
            self.api_client.set_token(token_data["access_token"])
            self.api_client.config_manager.update_token(token_data["access_token"])

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
            self.logger.error(f"Login error: {str(e)}")
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