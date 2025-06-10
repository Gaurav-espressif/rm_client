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
        print("Default server endpoint updated")
    except Exception as e:
        print(f"Error updating server endpoint: {e}")

@server.command()
@click.pass_context
def reset(ctx):
    """Reset server configuration to default"""
    try:
        config_manager = ConfigManager()
        config_manager.reset_to_default()
        print("Default server configuration reset to default")
    except Exception as e:
        print(f"Error resetting server configuration: {e}")

@server.command()
@click.pass_context
def show(ctx):
    """Show current server endpoint"""
    try:
        config_manager = ConfigManager()
        endpoint = config_manager.get_base_url()
        print("\nStatus Code: 200")
        print("Response Body:")
        print(json.dumps({
            "status": "success",
            "description": "Current server endpoint",
            "endpoint": endpoint
        }, indent=2))
    except Exception as e:
        print("\nStatus Code: 400")
        print("Response Body:")
        print(json.dumps({
            "status": "error",
            "description": str(e)
        }, indent=2))

@server.command()
@click.option('--days', default=30, help="Maximum age of config files in days")
@click.pass_context
def cleanup(ctx, days):
    """Clean up old configuration files"""
    try:
        config_manager = ConfigManager()
        config_manager.cleanup_old_configs(days)
        print("\nStatus Code: 200")
        print("Response Body:")
        print(json.dumps({
            "status": "success",
            "description": "Cleanup completed successfully"
        }, indent=2))
    except Exception as e:
        print("\nStatus Code: 400")
        print("Response Body:")
        print(json.dumps({
            "status": "error",
            "description": str(e)
        }, indent=2)) 