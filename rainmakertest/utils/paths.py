"""
Centralized path management for the Rainmaker CLI tool.
All path-related operations should use these functions.
"""
from pathlib import Path
import os
import sys
from .logging_config import get_logger

logger = get_logger(__name__)

def get_project_root() -> Path:
    """Get the project root directory."""
    # Get the absolute path of the current file
    current_file = Path(__file__).resolve()
    # Go up to rainmakertest directory
    project_root = current_file.parent.parent
    logger.debug(f"Project root: {project_root}")
    return project_root

def get_user_config_dir() -> Path:
    """Get the user's configuration directory."""
    config_dir = Path.home() / ".rainmaker"
    config_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"User config directory: {config_dir}")
    return config_dir

def get_logs_dir() -> Path:
    """Get the logs directory."""
    logs_dir = get_user_config_dir() / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Logs directory: {logs_dir}")
    return logs_dir

def get_tokens_dir() -> Path:
    """Get the tokens directory."""
    tokens_dir = get_user_config_dir() / "tokens"
    tokens_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Tokens directory: {tokens_dir}")
    return tokens_dir

def get_firmware_dir() -> Path:
    """Get the firmware directory."""
    firmware_dir = get_user_config_dir() / "firmware"
    firmware_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Firmware directory: {firmware_dir}")
    return firmware_dir

def get_temp_dir() -> Path:
    """Get the temporary directory for configs."""
    temp_dir = Path("temp/rainmaker")
    temp_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Temp directory: {temp_dir}")
    return temp_dir

def get_default_config_path() -> Path:
    """Get the path to the default configuration file."""
    config_path = get_temp_dir() / "default.json"
    logger.debug(f"Default config path: {config_path}")
    return config_path

def get_user_config_path(config_id: str) -> Path:
    """Get the path to a user-specific configuration file."""
    config_path = get_temp_dir() / f"{config_id}.json"
    logger.debug(f"User config path: {config_path}")
    return config_path

def get_user_token_path(config_id: str) -> Path:
    """Get the path to a user-specific token file."""
    config_path = get_temp_dir() / f"{config_id}.json"
    logger.debug(f"User token path: {config_path}")
    return config_path

def ensure_directory_exists(path: Path) -> None:
    """Ensure a directory exists, creating it if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {path}")
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise 