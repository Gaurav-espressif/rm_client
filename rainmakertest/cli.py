import os
import click
from typing import Optional, List
import logging

from rainmakertest.utils.email_service import EmailService
from .utils.api_client import ApiClient
from .auth.login_service import LoginService
from .user.user_service import UserService
from .admin.admin_user_service import AdminUserService
from .ota.ota_image_service import OTAService
from .ota.ota_job_service import OTAJobService
from .utils.token_json_load import prettify
from .nodes.node_service import NodeService
from .nodes.node_admin_service import NodeAdminService
from tabulate import tabulate
import json
from pathlib import Path
from .utils.config import update_base_url, get_config_path, get_base_url
from .utils.config_manager import ConfigManager

# Import modularized CLI commands
from .services.auth.cli import login, logout
from .services.user.cli import user
from .services.admin.cli import admin
from .services.ota.cli import ota
from .services.node.cli import node
from .services.email.cli import email
from .services.server.cli import server
from .services.create.cli import create

@click.group()
@click.option('--debug', is_flag=True, help="Enable debug logging")
@click.option('--config', required=False, help="Configuration ID (UUID) to use")
@click.pass_context
def cli(ctx, debug, config):
    """Rainmaker CLI Tool"""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ctx.ensure_object(dict)
    
    # Only create API client and services if config is provided
    if config:
        api_client = ApiClient(config_id=config)
        ctx.obj['api_client'] = api_client
        ctx.obj['login_service'] = LoginService(api_client)
        ctx.obj['user_service'] = UserService(api_client)
        ctx.obj['admin_service'] = AdminUserService(api_client)
        ctx.obj['ota_image_service'] = OTAService(api_client)
        ctx.obj['ota_job_service'] = OTAJobService(api_client)
        ctx.obj['node_service'] = NodeService(api_client)
        ctx.obj['node_admin_service'] = NodeAdminService(api_client)
        ctx.obj['config_id'] = config
    else:
        # For commands other than login, try to use default config
        try:
            # Create API client without config_id to use default config.json/token.json
            api_client = ApiClient()
            
            # Verify if we have a valid token
            if not api_client.config_manager.get_token():
                raise ValueError("No valid token found")
                
            ctx.obj['api_client'] = api_client
            ctx.obj['login_service'] = LoginService(api_client)
            ctx.obj['user_service'] = UserService(api_client)
            ctx.obj['admin_service'] = AdminUserService(api_client)
            ctx.obj['ota_image_service'] = OTAService(api_client)
            ctx.obj['ota_job_service'] = OTAJobService(api_client)
            ctx.obj['node_service'] = NodeService(api_client)
            ctx.obj['node_admin_service'] = NodeAdminService(api_client)
        except (FileNotFoundError, ValueError) as e:
            # Only raise error for non-login commands
            if ctx.invoked_subcommand != 'login':
                click.echo("Please login first using 'rmcli login user'")
                raise click.Abort()
            # For login command, create a basic API client without config
            api_client = ApiClient()
            ctx.obj['api_client'] = api_client
            ctx.obj['login_service'] = LoginService(api_client)

# Register all command groups
cli.add_command(login)
cli.add_command(logout)
cli.add_command(user)
cli.add_command(create)
cli.add_command(ota)
cli.add_command(node)
cli.add_command(email)
cli.add_command(server)

if __name__ == '__main__':
    cli()