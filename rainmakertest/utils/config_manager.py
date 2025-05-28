import json
import os
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
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
        # Get the project root directory (rainmakertest)
        project_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Create temp/rainmaker directory if it doesn't exist
        self.config_dir = project_dir / "temp" / "rainmaker"
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _get_config_path(self) -> Path:
        """Get the path to the config file based on UUID or default."""
        if not self.config_id:
            # Return path to default config.json
            return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "config.json"
        return self.config_dir / f"{self.config_id}.json"

    def _get_token_path(self) -> Path:
        """Get the path to the token file."""
        if not self.config_id:
            # Return path to default token.json
            return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "token.json"
        return self.config_dir / f"{self.config_id}_token.json"

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
        """Save configuration to file with atomic write."""
        if not self._config_data:
            raise ValueError("No configuration data to save")

        try:
            # Validate before saving
            self._validate_config(self._config_data)
            
            # Create a temporary file
            temp_file = self._get_config_path().with_suffix('.tmp')
            
            # Write to temporary file
            with open(temp_file, 'w') as f:
                json.dump(self._config_data, f, indent=4)
            
            # Atomic rename
            temp_file.replace(self._get_config_path())
            
            # Set appropriate file permissions (read/write for owner only)
            os.chmod(self._get_config_path(), 0o600)
            
            self.logger.debug(f"Saved config to {self._get_config_path()}")

            # If using default config, also save token to token.json
            if not self.config_id and 'session' in self._config_data:
                token_data = {'access_token': self._config_data['session'].get('access_token')}
                token_path = self._get_token_path()
                with open(token_path, 'w') as f:
                    json.dump(token_data, f, indent=4)
                os.chmod(token_path, 0o600)
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
        if not token:
            raise ValueError("Token cannot be empty")

        # For default case (no config_id), only update token.json
        if not self.config_id:
            token_path = self._get_token_path()
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
        """Clean up old config files."""
        try:
            current_time = datetime.utcnow()
            for config_file in self.config_dir.glob("*.json"):
                if config_file.name == "config.json":
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
            token_path = self.config_dir / f"{config_id}_token.json"
            if token_path.exists():
                token_path.unlink() 