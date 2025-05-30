import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...auth.login_service import LoginService
from ...utils.config_manager import ConfigManager

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

        if result.get("status") == "success":
            click.echo(f"Login successful. Access token: {result['token']['access_token'][:15]}...")
        else:
            click.echo(f"Login failed: {result.get('message', 'Unknown error')}")
        return

    # Handle default case (no endpoint provided)
    if not endpoint:
        try:
            # Try to get the default endpoint from config.json
            endpoint = config_manager.get_base_url()
        except FileNotFoundError:
            click.echo("No default configuration found. Please specify --endpoint or run 'rmcli server reset'")
            return

        # Create API client with default config
        api_client = ApiClient()
        login_service = LoginService(api_client)
        
        # Update context with new instances
        ctx.obj['api_client'] = api_client
        ctx.obj['login_service'] = login_service

        # Attempt login
        result = login_service.login_user(username, password)

        if result.get("status") == "success":
            click.echo(f"Login successful. Access token: {result['token']['access_token'][:15]}...")
        else:
            click.echo(f"Login failed: {result.get('message', 'Unknown error')}")
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
        click.echo(f"Login successful. Access token: {result['token']['access_token'][:15]}...")
        click.echo(f"Configuration ID: {config_id}")
        click.echo("Use this ID with --config option for subsequent commands")
    else:
        click.echo(f"Login failed: {result.get('message', 'Unknown error')}")

@click.command()
@click.pass_context
def logout(ctx):
    """Logout current user by clearing tokens"""
    try:
        api_client = ctx.obj['api_client']

        # Clear client-side tokens
        api_client.clear_token()

        click.echo("Successfully logged out")
    except Exception as e:
        click.echo(f"Logout failed: {str(e)}")
        raise click.Abort() 
