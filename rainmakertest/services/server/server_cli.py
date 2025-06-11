import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...utils.config_manager import ConfigManager
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

@click.group()
def server():
    """Server management commands"""
    pass

@server.command()
@click.option('--endpoint', help="New HTTP base URL endpoint")
@click.pass_context
def update(ctx, endpoint):
    """Update server endpoint"""
    if not endpoint:
        endpoint = click.prompt("Enter new server endpoint")

    try:
        config_manager = ConfigManager()
        config_manager.update_base_url(endpoint)
        click.echo(json.dumps({
            "status": "success",
            "description": "Server endpoint updated",
            "endpoint": endpoint
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@server.command()
@click.pass_context
def reset(ctx):
    """Reset server configuration to default"""
    try:
        config_manager = ConfigManager()
        config_manager.reset_to_default()
        click.echo(json.dumps({
            "status": "success",
            "description": "Server configuration reset to default"
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@server.command()
@click.pass_context
def show(ctx):
    """Show current server endpoint"""
    try:
        config_manager = ConfigManager()
        endpoint = config_manager.get_base_url()
        click.echo(json.dumps({
            "status": "success",
            "description": "Current server endpoint",
            "endpoint": endpoint
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@server.command()
@click.option('--days', default=30, help="Maximum age of config files in days")
@click.pass_context
def cleanup(ctx, days):
    """Clean up old configuration files"""
    try:
        config_manager = ConfigManager()
        config_manager.cleanup_old_configs(days)
        click.echo(json.dumps({
            "status": "success",
            "description": "Cleanup completed successfully"
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2)) 