import os
import click
from typing import Optional, List
import logging
from pathlib import Path
import json
from datetime import datetime

from ...utils.email_service import EmailService
from ...utils.api_client import ApiClient
from ...auth.login_service import LoginService
from ...user.user_service import UserService
from ...admin.admin_user_service import AdminUserService
from ...ota.ota_image_service import OTAService
from ...ota.ota_job_service import OTAJobService
from ...utils.token_json_load import prettify
from ...nodes.node_service import NodeService
from ...nodes.node_admin_service import NodeAdminService
from ...device_grouping.grouping import GroupingService
from ...timeseries.timeseries import TimeSeriesService
from ...event_filter.event_filter import EventFilterService
from ...role_policy_manager.role_policy import RolePolicyService
from ...moblie_platfrom_endpoint.moblie_platfrom_endpoint import MobilePlatformEndpointService
from ...utils.config_manager import ConfigManager
from ...utils.logging_config import setup_logging, get_logger
from ...utils.paths import get_user_config_path, get_temp_dir, get_project_root, get_user_config_dir, ensure_directory_exists

# Configure root logger only once
logger = logging.getLogger('rainmakertest')
logger.handlers = []  # Clear any existing handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    '%Y-%m-%d %H:%M:%S'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# Prevent duplicate logs
for name in logging.root.manager.loggerDict:
    if name.startswith('rainmakertest'):
        logging.getLogger(name).propagate = False

# Import modularized CLI commands
from ..auth.auth_cli import login, logout
from ..user.user_cli import user
from ..admin.admin_cli import admin
from ..ota.ota_cli import ota
from ..node.node_cli import node
from ..email.email_cli import email
from ..server.server_cli import server
from ..create.create_cli import create
from ..device_grouping.grouping_cli import grouping
from ..timeseries.timeseries_cli import timeseries
from ..event_filter.event_filter_cli import event_filter
from ..role_policy_manager.role_policy_cli import role_policy
from ..moblie_platfrom_endpoint.moblie_platfrom_endpoint_cli import mobile_platform

@click.group()
@click.option('--debug', is_flag=True, help="Enable debug logging")
@click.option('--config', help="Config ID to use")
@click.pass_context
def cli(ctx, debug, config):
    """Rainmaker CLI tool"""
    # Set up logging
    log_level = logging.DEBUG if debug else logging.INFO
    setup_logging()
    
    # Set logging level after setup
    if debug:
        logging.getLogger('rainmakertest').setLevel(logging.DEBUG)
    
    # Initialize context object
    ctx.ensure_object(dict)
    
    # Create API client with config ID if provided
    api_client = ApiClient(config)
    
    # Initialize services
    ctx.obj['api_client'] = api_client
    ctx.obj['login_service'] = LoginService(api_client)
    ctx.obj['user_service'] = UserService(api_client)
    ctx.obj['admin_service'] = AdminUserService(api_client)
    ctx.obj['email_service'] = EmailService()
    ctx.obj['ota_image_service'] = OTAService(api_client)
    ctx.obj['ota_job_service'] = OTAJobService(api_client)
    ctx.obj['node_service'] = NodeService(api_client)
    ctx.obj['node_admin_service'] = NodeAdminService(api_client)
    ctx.obj['grouping_service'] = GroupingService(api_client)
    ctx.obj['timeseries_service'] = TimeSeriesService(api_client)
    ctx.obj['event_filter_service'] = EventFilterService(api_client)
    ctx.obj['role_policy_service'] = RolePolicyService(api_client)
    ctx.obj['mobile_platform_service'] = MobilePlatformEndpointService(api_client)
    
    # Store config_id in context if provided
    if config:
        ctx.obj['config_id'] = config
        logger.debug(f"Using config ID: {config}")
        
        # Get config path using centralized path handling
        temp_dir = get_temp_dir()  # Already includes /temp/rainmaker
        config_path = temp_dir / f"{config}.json"
        
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            click.echo(f"Configuration file not found: {config_path}")
            raise click.Abort()
    else:
        # Use default config from user directory
        default_config_path = get_user_config_dir() / "default.json"
        if not default_config_path.exists():
            # Create default config with default URL
            default_config = {
                'environments': {
                    'http_base_url': 'https://api.rainmaker.espressif.com'
                },
                'session': {
                    'created_at': datetime.utcnow().isoformat(),
                    'last_used': datetime.utcnow().isoformat(),
                    'access_token': None
                }
            }
            ensure_directory_exists(default_config_path.parent)
            with open(default_config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            logger.debug(f"Created default config at: {default_config_path}")
            
    # For commands that require authentication, verify token
    if ctx.invoked_subcommand not in ['login', 'create', 'email', 'server', 'user', 'grouping', 'timeseries', 'event_filter', 'role_policy', 'mobile_platform']:
        token = api_client.config_manager.get_token()
        if not token:
            logger.warning("No token found, login required")
            click.echo("Please login first using 'rmcli login user'")
            raise click.Abort()
        logger.debug("Token loaded from config")

# Add commands
cli.add_command(login)
cli.add_command(logout)
cli.add_command(user)
cli.add_command(admin)
cli.add_command(ota)
cli.add_command(node)
cli.add_command(email)
cli.add_command(server)
cli.add_command(create)
cli.add_command(grouping)
cli.add_command(timeseries)
cli.add_command(event_filter)
cli.add_command(role_policy)
cli.add_command(mobile_platform)

@server.command()
def reset():
    """Reset server configuration to default values."""
    try:
        config_manager = ConfigManager()
        config_manager.reset_config()
        click.echo("Default server configuration reset to default")
    except Exception as e:
        logger.error(f"Error resetting server configuration: {str(e)}")
        raise click.ClickException(f"Error resetting server configuration: {str(e)}")

@server.command()
@click.option('--endpoint', required=True, help='Server endpoint URL')
def update(endpoint):
    """Update server configuration."""
    try:
        config_manager = ConfigManager()
        config_manager.update_base_url(endpoint)
        click.echo("Default server endpoint updated")
    except Exception as e:
        logger.error(f"Error updating server configuration: {str(e)}")
        raise click.ClickException(f"Error updating server configuration: {str(e)}")

class MainCLI:
    def __init__(self, config_id: str = None, debug: bool = False):
        """Initialize the main CLI with optional config ID and debug mode."""
        self.config_id = config_id
        if debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Logging initialized at level: DEBUG")
        
        logger.debug(f"Using config ID: {config_id}")
        
        # Initialize services
        self.api_client = ApiClient(config_id)
        self.node_service = NodeService(self.api_client)
        self.user_service = UserService(self.api_client)
        
        # Load token if available
        try:
            config = ConfigManager(config_id).load_config()
            if config.get('session', {}).get('access_token'):
                logger.debug("Token loaded from config")
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")

    def map_node(self, node_id: str, secret_key: str) -> dict:
        """Map a node to the user's account."""
        return self.node_service.map_user_node(node_id, secret_key, "map")

    def unmap_node(self, node_id: str, secret_key: str) -> dict:
        """Unmap a node from the user's account."""
        return self.node_service.map_user_node(node_id, secret_key, "unmap")

    def get_mapping_status(self, request_id: str) -> dict:
        """Get the status of a node mapping request."""
        return self.node_service.get_mapping_status(request_id)

    def get_user_nodes(self) -> dict:
        """Get all nodes associated with the user."""
        return self.node_service.get_user_nodes()

    def get_node_config(self, node_id: str) -> dict:
        """Get configuration for a specific node."""
        return self.node_service.get_node_config(node_id)

    def get_node_status(self, node_id: str) -> dict:
        """Get online/offline status of a node."""
        return self.node_service.get_node_status(node_id)

    def update_node_metadata(self, node_id: str, metadata: dict) -> dict:
        """Update metadata for a specific node."""
        return self.node_service.update_node_metadata(node_id, metadata)

    def delete_node_tags(self, node_id: str, tags: list) -> dict:
        """Delete tags from a specific node."""
        return self.node_service.delete_node_tags(node_id, tags)

if __name__ == '__main__':
    cli() 