from typing import Dict, List, Optional, Union
from ..utils.api_client import ApiClient
import logging

class UserPublicProfileService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_public_profile(self, user_name: Optional[str] = None) -> Dict:
        """Fetch a user's public profile
        
        Args:
            user_name: Optional user_name to fetch profile for. If not provided, fetches current user's profile
        """
        endpoint = "/v1/user/public_profile"
        params = {}
        
        if user_name:
            params["user_name"] = user_name
            
        return self.api_client.get(endpoint, params=params)

    def update_public_profile(self, profile: Optional[Dict] = None) -> Dict:
        """Add a new or update an existing public profile
        
        Args:
            profile: Profile data to update. Can be:
                - Dict with key-value pairs to add/update
                - None to delete the profile (reset to empty)
                - Empty dict {} to leave profile unchanged
        """
        endpoint = "/v1/user/public_profile"
        
        # Handle different profile update scenarios
        if profile is None:
            # Delete profile (reset to empty)
            data = {"profile": None}
        else:
            # Update profile with provided data
            data = {"profile": profile}
            
        return self.api_client.put(endpoint, json=data)
