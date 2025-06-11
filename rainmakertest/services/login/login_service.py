from typing import Dict

class LoginService:
    def __init__(self, api_client, config_manager):
        self.api_client = api_client
        self.config_manager = config_manager

    def login(self, username: str, password: str) -> Dict:
        """Login user and get access token"""
        endpoint = "/v1/login"
        payload = {
            "user_name": username,
            "password": password
        }
        
        # Login doesn't require authentication
        response = self.api_client.post(endpoint, data=payload, authenticate=False)
        
        # If login successful, save the token
        if isinstance(response, dict) and response.get("status") == "success":
            self.config_manager.save_token(response.get("token", {}))
            
        return response 