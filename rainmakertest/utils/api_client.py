import requests
from typing import Optional, Dict, Any
from .config import get_base_url
from .token_store import TokenStore


class ApiClient:
    def __init__(self, api_type: str = "http"):
        self.base_url = get_base_url(api_type)
        self.session = requests.Session()
        self.token_store = TokenStore()

    def _set_auth_headers(self, token_data: Dict):
        """Set the authorization headers for the session."""
        self.session.headers.update({
            "Authorization": f"{token_data['access_token']}",
            "X-ID-Token": token_data.get("id_token", ""),
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def set_access_token(self, token: str, id_token: Optional[str] = None):
        """Set the access token and update headers."""
        token_data = {"access_token": token, "id_token": id_token}
        self.token_store.save_token(token_data)
        self._set_auth_headers(token_data)

    def get_token_data(self) -> Optional[Dict]:
        """Get the current token data"""
        return self.token_store.get_token()

    def clear_token(self):
        """Clear the stored token"""
        self.token_store.clear_token()
        self.session.headers.pop("Authorization", None)
        self.session.headers.pop("X-ID-Token", None)

    def request(self, method: str, endpoint: str,
                data: Optional[Dict] = None,
                json: Optional[Dict] = None,
                params: Optional[Dict] = None,
                authenticate: bool = True) -> Dict:
        """Generic request handler with standardized error responses"""
        url = f"{self.base_url}{endpoint}"

        try:
            # Get auth headers if needed
            headers = {}
            if authenticate:
                token_data = self.token_store.get_token()
                if not token_data or not token_data.get("access_token"):
                    return {
                        "status": "failure",
                        "description": "Not logged in. Please use the 'login' command first",
                        "error_code": 401
                    }
                headers.update({
                    "Authorization": token_data["access_token"],
                    "X-ID-Token": token_data.get("id_token", "")
                })

            response = self.session.request(
                method,
                url,
                headers=headers,
                json=json or data,
                params=params,
                timeout=30
            )

            # Handle successful response
            response.raise_for_status()
            return {
                "status": "success",
                "data": response.json()
            }

        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors
            try:
                error_response = e.response.json()
                if isinstance(error_response, dict):
                    return {
                        "status": "failure",
                        "description": error_response.get("description", str(e)),
                        "error_code": e.response.status_code
                    }
            except ValueError:
                return {
                    "status": "failure",
                    "description": e.response.text or str(e),
                    "error_code": e.response.status_code
                }

        except Exception as e:
            # Handle other exceptions
            return {
                "status": "failure",
                "description": str(e),
                "error_code": 500
            }

    def post(self, endpoint: str,
             data: Optional[Dict] = None,
             json: Optional[Dict] = None,
             params: Optional[Dict] = None,
             authenticate: bool = True) -> Dict:
        return self.request("POST", endpoint, data=data, json=json, params=params, authenticate=authenticate)

    def get(self, endpoint: str,
            params: Optional[Dict] = None,
            authenticate: bool = True) -> Dict:
        return self.request("GET", endpoint, params=params, authenticate=authenticate)

    def put(self, endpoint: str,
            data: Optional[Dict] = None,
            json: Optional[Dict] = None,
            params: Optional[Dict] = None,
            authenticate: bool = True) -> Dict:
        return self.request("PUT", endpoint, data=data, json=json, params=params, authenticate=authenticate)

    def delete(self, endpoint: str,
               params: Optional[Dict] = None,
               authenticate: bool = True) -> Dict:
        return self.request("DELETE", endpoint, params=params, authenticate=authenticate)