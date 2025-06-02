import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...utils.config_manager import ConfigManager
from ...utils.config import update_base_url, get_config_path, get_base_url, get_current_config, update_config, reset_to_default
import os
import json
from datetime import datetime, timedelta

@click.group()
def server():
    """Server operations"""
    pass

@server.command()
@click.option('--endpoint', help="New HTTP base URL endpoint")
@click.option('--config', help="Custom config file path")
@click.pass_context
def update(ctx, endpoint, config):
    """Update server endpoint URL"""
    if not endpoint:
        endpoint = click.prompt("New endpoint URL")

    try:
        # Update the base URL in config
        if config:
            # Use custom config if provided
            config_manager = ConfigManager(config_id=config)
            config_manager.update_base_url(endpoint)
        else:
            # Use common config
            update_config({
                'environments': {
                    'http_base_url': endpoint
                }
            })
        click.echo(f"Server endpoint updated to: {endpoint}")
    except Exception as e:
        click.echo(f"Failed to update server endpoint: {str(e)}")
        raise click.Abort()

@server.command()
@click.option('--config', help="Custom config file path")
@click.pass_context
def reset(ctx, config):
    """Reset server configuration to default"""
    try:
        if config:
            # Use custom config if provided
            config_manager = ConfigManager(config_id=config)
            config_manager.reset_to_default()
        else:
            # Use common config
            reset_to_default()
        click.echo("Server configuration reset to default")
    except Exception as e:
        click.echo(f"Failed to reset server configuration: {str(e)}")
        raise click.Abort()

@server.command()
@click.option('--config', help="Custom config file path")
@click.pass_context
def show(ctx, config):
    """Show current server endpoint"""
    try:
        if config:
            # Use custom config if provided
            config_manager = ConfigManager(config_id=config)
            endpoint = config_manager.get_base_url()
        else:
            # Use common config
            endpoint = get_base_url()
        
        if endpoint:
            click.echo(f"Current server endpoint: {endpoint}")
        else:
            click.echo("No server endpoint configured.")
    except Exception as e:
        click.echo(f"Failed to show server endpoint: {str(e)}")
        raise click.Abort()

@server.command()
@click.option('--days', type=int, default=30, help="Maximum age of config files in days")
@click.pass_context
def cleanup(ctx, days):
    """Clean up old configuration files"""
    try:
        # Get the config directory
        config_dir = os.path.dirname(get_config_path())
        
        # Calculate the cutoff date
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # List all files in the config directory
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(config_dir, filename)
                
                # Get file modification time
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Delete if older than cutoff
                if mod_time < cutoff_date:
                    os.remove(file_path)
                    click.echo(f"Removed old config file: {filename}")
        
        click.echo(f"Cleanup completed. Removed config files older than {days} days")
    except Exception as e:
        click.echo(f"Failed to clean up configuration files: {str(e)}")
        raise click.Abort() 