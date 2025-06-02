import os
import time
import json
from typing import Optional, Dict, Union

class TokenStore:
    def __init__(self, token_file: str = None):
        self.token_file = token_file or self._get_default_token_path()
        self._ensure_token_dir()

    def _get_default_token_path(self):
        """Get default path for token storage"""
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(project_dir, "token.json")

    def _ensure_token_dir(self):
        """Ensure token directory exists"""
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)

    def save_token(self, token_data: Dict):
        """Save token with proper formatting"""
        try:
            with open(self.token_file, 'w') as f:
                json.dump({
                    'access_token': token_data.get('access_token', ''),
                    'id_token': token_data.get('id_token', ''),
                    'refresh_token': token_data.get('refresh_token', ''),
                    'timestamp': time.time()  # Add timestamp for validation
                }, f)
            os.chmod(self.token_file, 0o600)  # Secure file permissions
        except Exception as e:
            raise RuntimeError(f"Token save failed: {str(e)}")

    def get_token(self) -> Optional[Dict]:
        """Get token with validation"""
        if not os.path.exists(self.token_file):
            return None

        try:
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
                if not token_data.get('access_token'):
                    return None
                return token_data
        except Exception:
            return None

    def clear_token(self):
        """Completely clear the token storage"""
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
            # Also clear any in-memory tokens
            self._current_token = None
        except Exception as e:
            raise RuntimeError(f"Failed to clear token: {str(e)}")