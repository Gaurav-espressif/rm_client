from typing import Dict, Optional
from ..utils.api_client import ApiClient


class AdminUserService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def create_admin_user(
            self,
            user_name: str,
            super_admin: bool = False,
            locale: str = "no_locale"
    ) -> Dict:
        """Create a new admin or superadmin user"""
        endpoint = "/v1/admin/user2"
        params = {"locale": locale} if locale != "no_locale" else None
        payload = {
            "user_name": user_name,
            "super_admin": super_admin
        }
        return self.api_client.post(endpoint, data=payload, params=params)

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