import click
import json
from ...utils.api_client import ApiClient
from ...utils.config_manager import ConfigManager
from .login_service import LoginService

@click.group()
def login():
    """Login commands"""
    pass

@login.command()
@click.option('--username', help="Username (email or phone)")
@click.option('--password', help="Password")
@click.option('--endpoint', help="Server endpoint URL")
@click.pass_context
def user(ctx, username, password, endpoint):
    """Login with username and password"""
    if not username:
        username = click.prompt("Username")
    if not password:
        password = click.prompt("Password", hide_input=True)
    
    # Update endpoint if provided
    if endpoint:
        config_manager = ConfigManager()
        config_manager.update_base_url(endpoint)
    
    # Initialize services
    api_client = ApiClient()
    login_service = LoginService(api_client, config_manager)
    
    # Perform login
    result = login_service.login(username, password)
    click.echo(json.dumps(result, indent=2)) 