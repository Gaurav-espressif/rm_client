from rm_client.rainmakertest.utils.config_manager import ConfigManager
from rm_client.rainmakertest.utils.logging_config import setup_logging, get_logger

# Set up logging with debug level
setup_logging(level="DEBUG")
logger = get_logger(__name__)

# Initialize ConfigManager
cm = ConfigManager()
logger.info(f"Config path: {cm._get_config_path()}")
logger.info("Updating base URL...")

# Update base URL
cm.update_base_url('abc.com')
logger.info("Base URL updated successfully") 