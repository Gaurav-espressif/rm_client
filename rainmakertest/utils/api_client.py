import requests
from typing import Optional, Dict, Any
from .config import get_base_url
from .token_store import TokenStore

class ApiClient:
    def __init__(self, api_type: str = "http"):
        self.base_url = get_base_url(api_type)
        self.session = requests.Session()
        self.token_store = TokenStore()
        # Do NOT load auth headers here

        # Load existing token (but don't fail if it doesn't exist)
        token_data = self.token_store.get_token()
        if token_data and token_data.get("access_token"):
            self._set_auth_headers(token_data)

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
                authenticate: bool = True) -> Dict:  # Add an authenticate flag
        """Generic request handler with optional auth headers"""
        url = f"{self.base_url}{endpoint}"

        headers = {}
        if authenticate:
            token_data = self.token_store.get_token()
            if not token_data or not token_data.get("access_token"):
                raise Exception("Not logged in. Please use the 'login' command first.")
            headers.update({
                "Authorization": f"{token_data['access_token']}",
                "X-ID-Token": token_data.get("id_token", "")
            })
            self.session.headers.update(headers) # Ensure session headers are updated

        try:
            response = self.session.request(
                method,
                url,
                headers=self.session.headers, # Use session headers
                json=json or data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}")
            if e.response.status_code == 401 and authenticate:  # Only try refresh if authentication was intended
                self._refresh_token()
                return self.request(method, endpoint, data=data, json=json, params=params, authenticate=True)
            raise
        except Exception as e:
            print(f"Request failed: {str(e)}")
            if "token" in str(e).lower():
                self.token_store.clear_token()
            raise

    def post(self, endpoint: str,
             data: Optional[Dict] = None,
             json: Optional[Dict] = None,
             params: Optional[Dict] = None,
             authenticate: bool = True) -> Dict:
        """Authenticated POST request"""
        return self.request("POST", endpoint, data=data, json=json, params=params, authenticate=authenticate)

    def get(self, endpoint: str,
            params: Optional[Dict] = None,
            authenticate: bool = True) -> Dict:
        """Authenticated GET request"""
        return self.request("GET", endpoint, params=params, authenticate=authenticate)

    def put(self, endpoint: str,
            data: Optional[Dict] = None,
            json: Optional[Dict] = None,
            params: Optional[Dict] = None,
            authenticate: bool = True) -> Dict:
        """Authenticated PUT request"""
        return self.request("PUT", endpoint, data=data, json=json, params=params, authenticate=authenticate)

    def delete(self, endpoint: str,
               params: Optional[Dict] = None,
               authenticate: bool = True) -> Dict:
        """Authenticated DELETE request"""
        return self.request("DELETE", endpoint, params=params, authenticate=authenticate)

    def _refresh_token(self):
        """Refresh token using refresh token"""
        refresh_token = self.token_store.get_token('refresh_token')
        if not refresh_token:
            self.clear_token()
            raise Exception("No refresh token available. Please log in again.")

        endpoint = "/v1/refresh"  # Use the correct refresh endpoint
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            json={"refresh_token": refresh_token}
        )
        new_tokens = response.json()
        if 'accesstoken' not in new_tokens:
            self.clear_token()
            raise Exception(f"Token refresh failed: {new_tokens}")
        self.token_store.save_token({
            'access_token': new_tokens['accesstoken'],
            'refresh_token': new_tokens.get('refreshtoken', refresh_token),
            'id_token': new_tokens.get('idtoken', '')
        })
        self.set_access_token(new_tokens['accesstoken'], new_tokens.get('idtoken'))
