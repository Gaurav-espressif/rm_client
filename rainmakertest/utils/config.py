import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory."""
    # Start from the current file's directory
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    # Navigate up to the project root (where setup.py is located)
    while current_dir.name != 'rainmakertest' and current_dir.parent != current_dir:
        current_dir = current_dir.parent
    return current_dir

# Get the project root directory
PROJECT_ROOT = get_project_root()

# Define the path to config.json relative to project root
CONFIG_FILE = PROJECT_ROOT / "config.json"

# Default public URLs
DEFAULT_PUBLIC_URLS = {
    'environments': {
        'http_base_url': 'https://api.rainmaker.espressif.com'
    }
}

# Cache for base URLs to avoid repeated file reads
_base_urls = {
    "http": None,
    "rest": None
}

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found at: {CONFIG_FILE}")

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
    except IOError as e:
        raise RuntimeError(f"Failed to read config file: {e}")


def get_base_url(api_type: str = "http") -> str:
    """Get base URL from config for specified API type"""
    global _base_urls

    # Return cached value if available
    if _base_urls.get(api_type.lower()):
        return _base_urls[api_type.lower()]

    config = load_config()
    urls = {
        "http": config['environments']['http_base_url']
    }

    # Cache the values
    _base_urls["http"] = urls["http"]

    return urls.get(api_type.lower(), urls["http"])


def update_base_url(api_type: str, new_url: str) -> None:
    """Update the base URL in memory cache"""
    global _base_urls
    _base_urls[api_type.lower()] = new_url.rstrip('/')


def get_config_path() -> str:
    """Get the absolute path to config.json"""
    return CONFIG_FILE


def update_config(updates: Dict[str, Any]) -> None:
    """
    Update the config.json file with new values
    Args:
        updates: Dictionary with the structure to update (e.g., {'environments': {'http_base_url': 'new_url'}})
    """
    config = load_config()

    # Deep merge updates into existing config
    for key, value in updates.items():
        if isinstance(value, dict) and key in config:
            config[key].update(value)
        else:
            config[key] = value

    # Write updated config back to file
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

    # Update cached URLs if they were changed
    if 'environments' in updates:
        if 'http_base_url' in updates['environments']:
            update_base_url('http', updates['environments']['http_base_url'])
        if 'rest_base_url' in updates['environments']:
            update_base_url('rest', updates['environments']['rest_base_url'])


def reset_to_default() -> None:
    """Reset all endpoints to Espressif public URLs"""
    update_config(DEFAULT_PUBLIC_URLS)


def get_current_config() -> Dict[str, Any]:
    """Get the current configuration"""
    return load_config()