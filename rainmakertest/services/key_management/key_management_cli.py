import click
from typing import Optional, List, Dict
import json
import logging
from ...key_management.key_management import KeyManagementService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def key():
    """Key management operations"""
    pass

@key.command()
@click.option('--key-name', required=True, help='Name of the key (max 256 chars, alphanumeric, /, _, -)')
@click.option('--key-spec', required=True, 
              type=click.Choice(['ECDSA-P256', 'RSA-3072'], case_sensitive=False),
              help='Key specification (ECDSA-P256 or RSA-3072)')
@click.option('--description', help='Optional description for the key')
@click.option('--tags', multiple=True, 
              help='Tags in format key:val (can specify multiple)')
@click.pass_context
def create(ctx, key_name: str, key_spec: str, description: Optional[str], tags: List[str]):
    """Create a new key"""
    try:
        api_client = ctx.obj['api_client']
        key_service = KeyManagementService(api_client)
        
        # Convert tags to list if provided
        tags_list = list(tags) if tags else None
        
        result = key_service.create_key(
            key_name=key_name,
            key_spec=key_spec,
            description=description,
            tags=tags_list
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating key: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@key.command()
@click.option('--key-name', help='Name of the key to get details for (optional - returns all keys if not specified)')
@click.pass_context
def get(ctx, key_name: Optional[str]):
    """Get details and digest of the key(s)"""
    try:
        api_client = ctx.obj['api_client']
        key_service = KeyManagementService(api_client)
        
        result = key_service.get_key(key_name=key_name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting key details: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
