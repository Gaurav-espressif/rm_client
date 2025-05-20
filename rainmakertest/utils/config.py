import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Get the directory where this script (config.py) is located
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to reach the project root (r_maker_client/)
PROJECT_ROOT = os.path.dirname(UTILS_DIR)

# Define the absolute path to config.json (now in project root)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")

# Default public URLs
DEFAULT_PUBLIC_URLS = {
    'environments': {
        'http_base_url': 'https://api.rainmaker.espressif.com',
        'rest_base_url': 'https://api.rainmaker.espressif.com',
        'dashboard_url': 'https://dashboard.rainmaker.espressif.com/login'
    }
}

# Cache for base URLs to avoid repeated file reads
_base_urls = {
    "http": None,
    "rest": None
}
def load_config() -> Dict[str, Any]:
    """Load configuration from config.json using absolute path"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found at: {CONFIG_FILE}")

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def get_base_url(api_type: str = "http") -> str:
    """Get base URL from config for specified API type"""
    global _base_urls

    # Return cached value if available
    if _base_urls.get(api_type.lower()):
        return _base_urls[api_type.lower()]

    config = load_config()
    urls = {
        "http": config['environments']['http_base_url'],
        "rest": config['environments']['rest_base_url']
    }

    # Cache the values
    _base_urls["http"] = urls["http"]
    _base_urls["rest"] = urls["rest"]

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