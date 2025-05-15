import json
import os
from typing import Dict, Any

# Get the directory where this script (config.py) is located
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the absolute path to config.json
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json using absolute path"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found at: {CONFIG_FILE}")

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def get_base_url(api_type: str = "http") -> str:
    """Get base URL from config for specified API type"""
    config = load_config()
    urls = {
        "http": config['environments']['http_base_url'],
        "rest": config['environments']['rest_base_url']
    }
    return urls.get(api_type.lower(), config['environments']['http_base_url'])