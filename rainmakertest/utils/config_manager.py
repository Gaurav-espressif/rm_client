import requests
from typing import Optional, Dict, Any, List
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
        self._ensure_config_dir()
        self._config_data = None

    def _ensure_config_dir(self):
        """Ensure the config directory exists"""
        # Create temp/rainmaker directory
        self.config_dir = Path("temp/rainmaker")
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _get_config_path(self) -> Path:
        """Get the path to the config file based on UUID or default."""
        if not self.config_id:
            return self.config_dir / "default.json"
        return self.config_dir / f"{self.config_id}.json"

    def _get_token_path(self) -> Path:
        """Get the path to the token file."""
        if not self.config_id:
            return self.config_dir / "default.json"
        return self.config_dir / f"{self.config_id}.json"

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration structure and required fields."""
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        if 'environments' not in config:
            raise ValueError("Configuration missing 'environments' section")
        
        if 'http_base_url' not in config['environments']:
            raise ValueError("Configuration missing 'http_base_url' in environments section")

        if 'session' not in config:
            config['session'] = {}

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        config_path = self._get_config_path()
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, 'r') as f:
                try:
                    config = json.load(f)
                    self.logger.debug(f"Loaded config from {config_path}")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON in config file {config_path}: {e}")
                    raise ValueError(f"Invalid JSON format in configuration file: {e}")
                
                # Validate config structure
                try:
                    self._validate_config(config)
                except ValueError as e:
                    self.logger.error(f"Invalid config structure: {e}")
                    raise
                
                # If using default config, try to load token from token.json
                if not self.config_id:
                    token_path = self._get_token_path()
                    if token_path.exists():
                        try:
                            with open(token_path, 'r') as tf:
                                token_data = json.load(tf)
                                if 'session' not in config:
                                    config['session'] = {}
                                config['session']['access_token'] = token_data.get('access_token')
                        except (json.JSONDecodeError, IOError) as e:
                            self.logger.warning(f"Failed to load token file: {e}")
                
                return config
        except IOError as e:
            self.logger.error(f"Failed to read config file {config_path}: {e}")
            raise RuntimeError(f"Failed to read configuration file: {e}")

    def _save_config(self) -> None:
        """Save configuration to file."""
        if not self._config_data:
            raise ValueError("No configuration data to save")

        try:
            # Validate before saving
            self._validate_config(self._config_data)
            
            # Get the config path
            config_path = self._get_config_path()
            
            # Write directly to the file
            with open(config_path, 'w') as f:
                json.dump(self._config_data, f, indent=4)
            
            # Set appropriate file permissions (read/write for owner only)
            os.chmod(config_path, 0o600)
            
            self.logger.debug(f"Saved config to {config_path}")

        except Exception as e:
            logger.error(f"Error saving config to {self._get_config_path()}: {e}")
            raise

    def get_base_url(self) -> str:
        """Get the HTTP base URL from config."""
        config = self._load_config()
        return config['environments']['http_base_url']

    def update_base_url(self, new_url: str) -> None:
        """Update the HTTP base URL in config."""
        if not new_url:
            raise ValueError("Base URL cannot be empty")
            
        config = self._load_config()
        config['environments']['http_base_url'] = new_url.rstrip('/')
        config['session']['last_used'] = datetime.utcnow().isoformat()
        self._config_data = config
        self._save_config()

    def get_token(self) -> Optional[str]:
        """Get the access token from config."""
        config = self._load_config()
        return config.get('session', {}).get('access_token')

    def update_token(self, token: str) -> None:
        """Update the access token in the configuration"""
        # For default case (no config_id), only update token.json
        if not self.config_id:
            token_path = self._get_token_path()
            if not token:  # If clearing token (logout)
                if token_path.exists():
                    token_path.unlink()  # Delete the token file
                return
            token_data = {'access_token': token}
            with open(token_path, 'w') as f:
                json.dump(token_data, f, indent=4)
            os.chmod(token_path, 0o600)
            return

        # For custom endpoint case, update the UUID config file
        config = self._load_config()
        if 'session' not in config:
            config['session'] = {}
        config['session']['access_token'] = token
        config['session']['last_used'] = datetime.utcnow().isoformat()
        self._config_data = config
        self._save_config()

    def update_credentials(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """Update username and password in config."""
        config = self._load_config()
        if 'session' not in config:
            config['session'] = {}
        if username:
            config['session']['username'] = username
        if password:
            config['session']['password'] = password
        config['session']['last_used'] = datetime.utcnow().isoformat()
        self._config_data = config
        self._save_config()

    def create_new_config(self, endpoint: str, username: Optional[str] = None, 
                         password: Optional[str] = None) -> str:
        """Create a new config file with UUID and return the UUID."""
        if not endpoint:
            raise ValueError("Endpoint URL cannot be empty")
            
        new_uuid = str(uuid.uuid4())
        self.config_id = new_uuid
        self._config_data = {
            'environments': {
                'http_base_url': endpoint.rstrip('/')
            },
            'session': {
                'created_at': datetime.utcnow().isoformat(),
                'last_used': datetime.utcnow().isoformat()
            }
        }
        
        if username:
            self._config_data['session']['username'] = username
        if password:
            self._config_data['session']['password'] = password
            
        self._save_config()
        return new_uuid

    def cleanup_old_configs(self, max_age_days: int = 30) -> None:
        """Clean up old configuration files."""
        try:
            current_time = datetime.utcnow()
            for config_file in self.config_dir.glob("*.json"):
                if config_file.name == "default.json":
                    continue
                    
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        last_used = datetime.fromisoformat(config_data['session']['last_used'])
                        age_days = (current_time - last_used).days
                        
                        if age_days > max_age_days:
                            config_file.unlink()
                            logger.info(f"Removed old config file: {config_file}")
                except Exception as e:
                    logger.error(f"Error processing config file {config_file}: {e}")
        except Exception as e:
            logger.error(f"Error during config cleanup: {e}")

    def reset_to_default(self) -> None:
        """Reset configuration to default values."""
        self._config_data = {
            'environments': {
                'http_base_url': 'https://api.rainmaker.espressif.com'
            },
            'session': {
                'created_at': datetime.utcnow().isoformat(),
                'last_used': datetime.utcnow().isoformat()
            }
        }
        self._save_config()

    def save_config(self, config_data: Dict[str, Any]) -> str:
        """Save configuration to file and return the config ID"""
        if not self.config_id:
            self.config_id = str(uuid.uuid4())

        self._config_data = config_data
        self._save_config()
        return self.config_id

    def list_configs(self) -> List[str]:
        """List all available configuration IDs"""
        return [f.stem for f in self.config_dir.glob("*.json")]

    def delete_config(self, config_id: str) -> None:
        """Delete a configuration file"""
        if config_id:
            config_path = self.config_dir / f"{config_id}.json"
            if config_path.exists():
                config_path.unlink()
            token_path = self.config_dir / f"{config_id}.json"
            if token_path.exists():
                token_path.unlink()

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
                self.config_manager._config_data = self._config_data
                self.config_manager.save_config()
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