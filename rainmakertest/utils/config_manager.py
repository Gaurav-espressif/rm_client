import requests
from typing import Optional, Dict, Any
import logging
import os
from pathlib import Path
import json
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class ConfigManager:
    def __init__(self, config_id: Optional[str] = None):
        self.config_id = config_id
        self.logger = logging.getLogger(__name__)
        self._config_dir = self._get_config_dir()

    def _get_config_dir(self) -> Path:
        """Get the configuration directory path."""
        home = Path.home()
        config_dir = home / '.rainmaker'
        config_dir.mkdir(exist_ok=True)
        return config_dir

    def _get_config_path(self) -> Path:
        """Get the path to the configuration file."""
        if self.config_id:
            return self._config_dir / f"{self.config_id}.json"
        return self._config_dir / "default.json"

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        config_path = self._get_config_path()
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            raise

    def save_config(self, config_data: Dict[str, Any]) -> str:
        """Save configuration to file."""
        config_path = self._get_config_path()
        try:
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            return self.config_id or "default"
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            raise

    def create_new_config(self, endpoint: str, username: Optional[str] = None, 
                         password: Optional[str] = None) -> str:
        """Create a new config file with UUID and return the UUID."""
        if not endpoint:
            raise ValueError("Endpoint URL cannot be empty")
            
        new_uuid = str(uuid.uuid4())
        self.config_id = new_uuid
        
        config_data = {
            'environments': {
                'http_base_url': endpoint.rstrip('/')
            },
            'session': {
                'created_at': datetime.utcnow().isoformat(),
                'last_used': datetime.utcnow().isoformat()
            }
        }
        
        if username:
            config_data['session']['username'] = username
        if password:
            config_data['session']['password'] = password
            
        self.save_config(config_data)
        return new_uuid

    def update_token(self, token: str) -> None:
        """Update the access token in the configuration."""
        try:
            config = self._load_config()
        except FileNotFoundError:
            config = {"session": {}, "environments": {"http_base_url": ""}}
        
        if "session" not in config:
            config["session"] = {}
        
        config["session"]["access_token"] = token
        self.save_config(config)

    def get_token(self) -> Optional[str]:
        """Get the access token from the configuration."""
        try:
            config = self._load_config()
            return config.get("session", {}).get("access_token")
        except FileNotFoundError:
            return None

class ApiClient:
    def __init__(self, config_id: Optional[str] = None):
        self.config_manager = ConfigManager(config_id)
        self.config_id = config_id
        self.logger = logging.getLogger(__name__)
        self._config_data = None
        self._fallback_config = None

    def set_token(self, token: str) -> None:
        """Set the access token in the configuration."""
        if not token:
            raise ValueError("Token cannot be empty")
        self.config_manager.update_token(token)
        self._config_data = None  # Clear cached config to force reload

    def clear_token(self) -> None:
        """Clear the access token from the configuration."""
        try:
            # Set empty token in config
            self.config_manager.update_token("")
            self._config_data = None  # Clear cached config to force reload
        except Exception as e:
            raise RuntimeError(f"Failed to clear token: {str(e)}")

    def _load_config(self):
        """Load fresh config data for each request"""
        if not self._config_data:
            try:
                self._config_data = self.config_manager._load_config()
            except FileNotFoundError:
                # Try loading from old config system
                self._load_fallback_config()
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in config file: {e}")
                raise ValueError(f"Invalid configuration file format: {e}")
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                raise
        return self._config_data

    def _load_fallback_config(self):
        """Load configuration from old config.json/token.json system"""
        try:
            project_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = project_dir / "config.json"
            token_path = project_dir / "token.json"

            if not config_path.exists():
                raise FileNotFoundError("Neither new config nor old config.json found")

            with open(config_path, 'r') as f:
                self._config_data = json.load(f)

            if token_path.exists():
                with open(token_path, 'r') as f:
                    token_data = json.load(f)
                    if 'session' not in self._config_data:
                        self._config_data['session'] = {}
                    self._config_data['session']['access_token'] = token_data.get('access_token')

            # Save the fallback config to the new location
            if self._config_data:
                self.config_id = self.config_manager.save_config(self._config_data)
        except Exception as e:
            self.logger.error(f"Error loading fallback config: {e}")
            raise

    def _get_headers(self, authenticate: bool = True) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if authenticate:
            config = self._load_config()
            token = config.get('session', {}).get('access_token')
            if not token:
                self.logger.warning("No access token found in configuration")
                raise ValueError("Authentication required but no access token found")
            headers['Authorization'] = token
        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and common error cases"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {str(e)}"
            if response.status_code == 401:
                error_msg = "Authentication failed - token may be expired"
            elif response.status_code == 403:
                error_msg = "Access forbidden - check permissions"
            elif response.status_code == 404:
                error_msg = "Resource not found"
            elif response.status_code == 500:
                error_msg = "Server error - please try again later"
            
            self.logger.error(error_msg)
            return {
                "status": "failure",
                "message": error_msg,
                "error_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, authenticate: bool = True) -> Dict[str, Any]:
        """Make a GET request to the API."""
        config = self._load_config()
        base_url = config['environments']['http_base_url']
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = self._get_headers(authenticate)
        
        try:
            response = requests.get(
                url, 
                headers=headers, 
                params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, 
             params: Optional[Dict[str, Any]] = None, authenticate: bool = True) -> Dict[str, Any]:
        """Make a POST request to the API."""
        config = self._load_config()
        base_url = config['environments']['http_base_url']
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = self._get_headers(authenticate)
        
        # --- DEBUG LOGGING ---
        self.logger.debug("POST Request:")
        self.logger.debug(f"URL: {url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Params: {params}")
        self.logger.debug(f"Payload: {json or data}")
        # ---------------------
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                json=json or data,
                params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, 
            params: Optional[Dict[str, Any]] = None, authenticate: bool = True) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        config = self._load_config()
        base_url = config['environments']['http_base_url']
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = self._get_headers(authenticate)
        
        # --- DEBUG LOGGING ---
        self.logger.debug("PUT Request:")
        self.logger.debug(f"URL: {url}")
        self.logger.debug(f"Headers: {headers}")
        self.logger.debug(f"Params: {params}")
        self.logger.debug(f"Payload: {json or data}")
        # ---------------------
        
        try:
            response = requests.put(
                url, 
                headers=headers, 
                json=json or data,
                params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }

    def delete(self, endpoint: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, authenticate: bool = True) -> Dict[str, Any]:
        """Make a DELETE request to the API."""
        config = self._load_config()
        base_url = config['environments']['http_base_url']
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        headers = self._get_headers(authenticate)
        
        try:
            response = requests.delete(
                url, 
                headers=headers, 
                json=json,
                params=params
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return {
                "status": "failure",
                "message": str(e),
                "error_code": 500
            }
