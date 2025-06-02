from typing import Dict, Optional
from ..utils.api_client import ApiClient


class AdminUserService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create_admin(
            self,
            user_name: str,
            quota: int
    ) -> Dict:
        """Create a new admin user with quota"""
        endpoint = "/v1/admin/user2"
        payload = {
            "user_name": user_name,
            "admin": True,
            "quota": quota
        }
        return self.api_client.post(endpoint, data=payload)

    def create_superadmin(
            self,
            user_name: str
    ) -> Dict:
        """Create a new superadmin user"""
        endpoint = "/v1/admin/user2"
        payload = {
            "user_name": user_name,
            "super_admin": True
        }
        return self.api_client.post(endpoint, data=payload)

    def get_user_details(
            self,
            user_name: Optional[str] = None,
            all_users: bool = False,
            admin: bool = False,
            superadmin: bool = False
    ) -> Dict:
        """Get user details with various filters"""
        endpoint = "/v1/admin/user2"
        params = {}

        if user_name:
            params["user_name"] = user_name
        if all_users:
            params["all"] = "true"
        if admin:
            params["admin"] = "true"
        if superadmin:
            params["superadmin"] = "true"

        return self.api_client.get(endpoint, params=params)