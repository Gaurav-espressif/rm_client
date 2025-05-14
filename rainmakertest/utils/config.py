import json
import os
from typing import Dict, Any

CONFIG_FILE = "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not found")

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