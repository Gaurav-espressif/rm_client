from utils.logging_config import setup_logging
from utils.token_store import TokenStore
import logging

def test_token_storage():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create token store
    token_store = TokenStore()
    
    # Test token
    test_token = {
        "access_token": "test_access_token",
        "id_token": "test_id_token",
        "refresh_token": "test_refresh_token"
    }
    
    # Save token
    logger.info("Testing token storage...")
    token_store.save_token(test_token)
    
    # Read token
    stored_token = token_store.get_token()
    logger.info(f"Stored token: {stored_token}")
    
    # Clear token
    token_store.clear_token()
    logger.info("Token cleared")
    
    # Verify token is cleared
    final_token = token_store.get_token()
    logger.info(f"Final token state: {final_token}")

if __name__ == "__main__":
    test_token_storage() 