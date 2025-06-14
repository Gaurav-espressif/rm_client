import logging
import os
import sys

def get_logger(name):
    """Get a logger instance with the specified name"""
    return logging.getLogger(name)

def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.expanduser("~"), ".rainmaker", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "rainmaker.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING) 