import os
from datetime import time

import json
from typing import Optional, Dict, Union


class TokenStore:
    def __init__(self, token_file: str = None):
        if token_file is None:
            # Store token.json in the rainmakertest directory
            project_dir = os.path.dirname(os.path.abspath(__file__))  # .../rainmakertest/utils
            project_root = os.path.dirname(project_dir)               # .../rainmakertest
            self.token_file = os.path.join(project_root, "token.json")
        else:
            self.token_file = os.path.abspath(os.path.expanduser(token_file))
        self._ensure_token_dir()

    def _ensure_token_dir(self):
        """Ensure the directory for token file exists"""
        try:
            token_dir = os.path.dirname(self.token_file)
            os.makedirs(token_dir, exist_ok=True)
        except Exception:
            # Fallback to current directory
            self.token_file = os.path.abspath(".rainmaker_token.json")
            try:
                os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            except Exception:
                raise

    def save_token(self, token_data: Dict):
        """Save token information"""
        try:
            self._ensure_token_dir()
            with open(self.token_file, 'w') as f:
                json.dump(token_data, f)
            try:
                os.chmod(self.token_file, 0o600)
            except Exception:
                pass
        except Exception as e:
            raise RuntimeError(f"Failed to save token: {str(e)}")

    def get_token(self, token_type: str = None) -> Optional[Union[Dict, str]]:
        """Get stored token or specific token type"""
        if not os.path.exists(self.token_file):
            return None

        try:
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)

                if not isinstance(token_data, dict):
                    return None
                if not token_data:
                    return None

                # If no specific type requested, return all token data
                if token_type is None:
                    return token_data
                # Otherwise return the specific token
                return token_data.get(token_type)

        except (json.JSONDecodeError, Exception):
            return None

    def validate_token(self, token_type: str = "access_token") -> bool:
        token = self.get_token(token_type)
        if not token:
            return False
        try:
            import jwt
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get("exp", 0) > time.time()
        except:
            return False


    def clear_token(self):
        """Remove stored token"""
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except Exception:
            pass