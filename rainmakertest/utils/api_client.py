import requests
from typing import Optional, Dict, Any
import logging
import os
from pathlib import Path
import json
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, config_id: Optional[str] = None):
        """Initialize API client with optional config ID."""
        self.config_manager = ConfigManager(config_id)
        self.config_id = config_id
        self.logger = logger  # Use the module-level logger
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

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration data."""
        if not self._config_data:
            try:
                self._config_data = self.config_manager._load_config()
            except FileNotFoundError as e:
                self.logger.error(f"Configuration file not found: {e}")
                raise
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in config file: {e}")
                raise ValueError(f"Invalid configuration file format: {e}")
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                raise
        return self._config_data

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration data."""
        if not self._config_data:
            try:
                self._config_data = self.config_manager._load_config()
            except FileNotFoundError as e:
                self.logger.error(f"Configuration file not found: {e}")
                raise
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON in config file: {e}")
                raise ValueError(f"Invalid configuration file format: {e}")
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                raise
        return self._config_data

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