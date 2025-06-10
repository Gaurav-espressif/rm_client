import logging
import os
from typing import Optional

class LoggerConfig:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not LoggerConfig._initialized:
            LoggerConfig._initialized = True
            self.logger = logging.getLogger('rainmakertest')
            self._configure_logger()

    def _configure_logger(self):
        """Configure the logger with proper formatting and handlers"""
        # Clear any existing handlers
        self.logger.handlers.clear()

        # Set format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Set default level
        self.logger.setLevel(logging.INFO)

    def set_debug(self, enable: bool = True):
        """Enable or disable debug logging"""
        level = logging.DEBUG if enable else logging.INFO
        self.logger.setLevel(level)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance
        
        Args:
            name: Optional name for the logger. If None, returns root logger
            
        Returns:
            logging.Logger: Configured logger instance
        """
        if name:
            return self.logger.getChild(name)
        return self.logger

    @staticmethod
    def sanitize_log_message(message: str) -> str:
        """Sanitize sensitive information from log messages
        
        Args:
            message: The log message to sanitize
            
        Returns:
            str: Sanitized message
        """
        # Truncate long tokens
        if 'token' in message.lower() and len(message) > 100:
            return message[:100] + '...[TRUNCATED]'
        return message

class SensitiveFilter(logging.Filter):
    """Filter to sanitize sensitive information in logs"""
    
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = LoggerConfig.sanitize_log_message(record.msg)
        return True

# Initialize the global logger configuration
logger_config = LoggerConfig()

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance
    
    Args:
        name: Optional name for the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logger_config.get_logger(name)

def set_debug(enable: bool = True):
    """Enable or disable debug logging globally
    
    Args:
        enable: True to enable debug logging, False for info level
    """
    logger_config.set_debug(enable) 