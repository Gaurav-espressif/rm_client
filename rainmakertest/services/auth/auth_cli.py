import click
from typing import Optional
import uuid
import json
from pathlib import Path
from ...utils.api_client import ApiClient
from ...auth.login_service import LoginService
from ...utils.config_manager import ConfigManager
from ...utils.logging_config import get_logger
from ...utils.paths import get_temp_dir, ensure_directory_exists

logger = get_logger(__name__)

@click.group()
def auth():
    """Authentication operations"""
    pass

@auth.command()
@click.option('--username', required=True, help='Username/email for login')
@click.option('--password', required=True, help='Password for login')
def login(username, password):
    """Login to Rainmaker."""
    try:
        api_client = ApiClient()
        response = api_client.post(
            'v1/login',
            data={
                'user_name': username,
                'password': password
            },
            authenticate=False
        )
        
        if response.get('status') == 'error':
            logger.error(f"Login failed: {response.get('description')}")
            raise click.ClickException(f"Login failed: {response.get('description')}")
            
        access_token = response.get('accesstoken')
        if not access_token:
            logger.error("No access token in response")
            raise click.ClickException("Login failed: No access token received")
            
        api_client.set_token(access_token)
        click.echo(f"Login successful. Access token: {access_token[:10]}...")
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise click.ClickException(f"Login failed: {str(e)}")

@auth.command()
@click.pass_context
def logout(ctx):
    """Logout from Rainmaker session."""
    try:
        config_id = ctx.obj.get('config_id') if ctx.obj else None
        api_client = ApiClient(config_id=config_id)
        
        # Call the logout2 endpoint
        response = api_client.post('v1/logout2')
        
        if response.get('status') == 'error':
            logger.error(f"Logout failed: {response.get('description')}")
            raise click.ClickException(f"Logout failed: {response.get('description')}")
            
        # Clear the token after successful logout
        api_client.clear_token()
        click.echo("Logged out successfully")
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        raise click.ClickException(f"Logout failed: {str(e)}")

@click.group()
def login():
    """Login operations"""
    pass

@login.command()
@click.option('--username', help="Username (email or phone)")
@click.option('--password', help="User password")
@click.option('--endpoint', help="Server endpoint URL")
@click.pass_context
def user(ctx, username, password, endpoint):
    """Login as regular user"""
    if not username:
        username = click.prompt("Username")
    if not password:
        password = click.prompt("Password", hide_input=True)

    try:
        if endpoint:
            # Generate UUID for the new config
            config_id = str(uuid.uuid4())
            logger.debug(f"Generated config ID: {config_id}")

            # Get temp directory path and ensure it exists
            temp_dir = get_temp_dir()  # Already includes /temp/rainmaker
            ensure_directory_exists(temp_dir)

            # Create config file path
            config_path = temp_dir / f"{config_id}.json"
            logger.debug(f"Creating new config at: {config_path}")

            # Initialize config data with the provided endpoint
            config_data = {
                'environments': {
                    'http_base_url': endpoint.rstrip('/')
                },
                'session': {}
            }

            # Save initial config
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=4)

            # Create API client with the new config
            api_client = ApiClient(config_id=config_id)
        else:
            # Use default config
            api_client = ApiClient()

        # Call the login2 endpoint with correct path
        response = api_client.post(
            '/v1/login2',
            data={
                'user_name': username,
                'password': password
            },
            authenticate=False
        )
        
        if isinstance(response, dict) and response.get('status') == 'failure':
            logger.error(f"Login failed: {response.get('description')}")
            raise click.ClickException(f"Login failed: {response.get('description')}")
            
        access_token = response.get('accesstoken')
        if not access_token:
            logger.error("No access token in response")
            raise click.ClickException("Login failed: No access token received")
            
        # Store the token
        api_client.set_token(access_token)

        if endpoint:
            click.echo(f"Login successful. Access token: {access_token[:10]}...")
            click.echo(f"Configuration ID: {config_id}")
            click.echo("Use this ID with --config option for subsequent commands")
        else:
            click.echo(f"Login successful. Access token: {access_token[:10]}...")
        
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise click.ClickException(f"Login failed: {str(e)}")

@click.command()
@click.pass_context
def logout(ctx):
    """Logout from Rainmaker session."""
    try:
        config_id = ctx.obj.get('config_id') if ctx.obj else None
        api_client = ApiClient(config_id=config_id)
        
        # Call the logout2 endpoint
        response = api_client.post('v1/logout2')
        
        if response.get('status') == 'error':
            logger.error(f"Logout failed: {response.get('description')}")
            raise click.ClickException(f"Logout failed: {response.get('description')}")
            
        # Clear the token after successful logout
        api_client.clear_token()
        click.echo("Logged out successfully")
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        raise click.ClickException(f"Logout failed: {str(e)}") 