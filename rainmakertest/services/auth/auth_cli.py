import click
from typing import Optional
import uuid
import json
from pathlib import Path
from ...utils.api_client import ApiClient
from ...auth.login_service import LoginService
from ...utils.config_manager import ConfigManager
from ...utils.logging_config import get_logger
from ...utils.paths import get_user_config_dir, ensure_directory_exists

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
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        # Try to extract server response from the error
        try:
            error_str = str(e)
            if "{'status':" in error_str:
                # Extract the JSON string from the error message
                start = error_str.find("{")
                end = error_str.rfind("}") + 1
                error_json = error_str[start:end]
                click.echo(error_json)
            else:
                click.echo(json.dumps({
                    "status": "failure",
                    "description": str(e),
                    "error_code": 500
                }, indent=2))
        except:
            click.echo(json.dumps({
                "status": "failure",
                "description": str(e),
                "error_code": 500
            }, indent=2))

@auth.command()
def logout():
    """Logout from Rainmaker session."""
    try:
        api_client = ApiClient()
        # Call the new logout2 endpoint
        response = api_client.post('v1/logout2')
        
        if response.get('status') == 'success':
            api_client.clear_token()
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

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
        # Create config manager
        config_manager = ConfigManager()

        # Check if we're using a specific config (--config flag was used)
        if hasattr(ctx, 'obj') and 'config_id' in ctx.obj:
            # Using specific config, create API client with that config
            api_client = ApiClient(config_id=ctx.obj['config_id'])
            login_service = LoginService(api_client)
            
            # Update context with new instances
            ctx.obj['api_client'] = api_client
            ctx.obj['login_service'] = login_service

            # Attempt login
            result = login_service.login_user(username, password)
            click.echo(json.dumps(result, indent=2))
            return

        # Handle default case (no endpoint provided)
        if not endpoint:
            try:
                # Try to get the default endpoint from default.json
                endpoint = config_manager.get_base_url()
            except FileNotFoundError:
                click.echo(json.dumps({
                    "status": "failure",
                    "description": "No default configuration found. Please specify --endpoint or run 'rmcli server reset'",
                    "error_code": 400
                }, indent=2))
                return

            # Create API client with default config
            api_client = ApiClient()
            login_service = LoginService(api_client)
            
            # Update context with new instances
            ctx.obj['api_client'] = api_client
            ctx.obj['login_service'] = login_service

            # Attempt login
            result = login_service.login_user(username, password)
            click.echo(json.dumps(result, indent=2))
            return

        # Handle custom endpoint case
        config_id = config_manager.create_new_config(
            endpoint=endpoint,
            username=username,
            password=password
        )

        # Create new API client with the new config
        api_client = ApiClient(config_id=config_id)
        
        # Create new login service with the new API client
        login_service = LoginService(api_client)
        
        # Update context with new instances
        ctx.obj['api_client'] = api_client
        ctx.obj['login_service'] = login_service
        ctx.obj['config_id'] = config_id

        # Attempt login with the new service
        result = login_service.login_user(username, password)
        if result.get("status") == "success":
            result["config_id"] = config_id
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@click.command()
@click.pass_context
def logout(ctx):
    """Logout current user by clearing tokens"""
    try:
        # Get the API client from context
        api_client = ctx.obj['api_client']
        
        # Get current token before clearing
        token = api_client.config_manager.get_token()
        if not token:
            click.echo(json.dumps({
                "status": "failure",
                "description": "No active token found",
                "error_code": 400
            }, indent=2))
            return

        # Get config ID before clearing
        config_id = api_client.config_id

        # Clear client-side tokens
        api_client.clear_token()

        # If using a specific config (UUID), delete the config file
        if config_id:
            api_client.config_manager.delete_config(config_id)

        click.echo(json.dumps({
            "status": "success",
            "description": "Successfully logged out",
            "error_code": 200
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort() 