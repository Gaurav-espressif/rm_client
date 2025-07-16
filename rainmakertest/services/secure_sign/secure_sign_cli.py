import click
from typing import Optional, List, Dict
import json
import logging
from ...secure_sign.secure_sign import SecureSignService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def secure_sign():
    """Secure sign operations"""
    pass

@secure_sign.command()
@click.option('--ota-image-id', required=True, help='ID of the OTA image to sign')
@click.option('--key-names', required=True, multiple=True,
              help='Key names to use for signing (can specify multiple)')
@click.option('--sign-boot-loader', is_flag=True, 
              help='Whether to sign the bootloader as well')
@click.pass_context
def create(ctx, ota_image_id: str, key_names: List[str], sign_boot_loader: bool):
    """Create a secure signing request for OTA images"""
    try:
        api_client = ctx.obj['api_client']
        secure_sign_service = SecureSignService(api_client)
        
        result = secure_sign_service.create_secure_sign(
            ota_image_id=ota_image_id,
            key_names=list(key_names),
            sign_boot_loader=sign_boot_loader
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating secure sign request: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@secure_sign.command()
@click.option('--request-id', required=True, help='ID of the signing request to check')
@click.pass_context
def status(ctx, request_id: str):
    """Get the status of a secure signing request"""
    try:
        api_client = ctx.obj['api_client']
        secure_sign_service = SecureSignService(api_client)
        
        result = secure_sign_service.get_secure_sign_status(request_id=request_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting secure sign status: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@secure_sign.command()
@click.option('--key-name', help='Name of the key to filter by')
@click.option('--num-records', type=int, help='Number of records to fetch')
@click.option('--start-id', help='Start ID for pagination')
@click.pass_context
def signed_images(ctx, key_name: Optional[str], num_records: Optional[int],
                 start_id: Optional[str]):
    """Get images signed by a specific key"""
    try:
        api_client = ctx.obj['api_client']
        secure_sign_service = SecureSignService(api_client)
        
        result = secure_sign_service.get_signed_images(
            key_name=key_name,
            num_records=num_records,
            start_id=start_id
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting signed images: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@secure_sign.command()
@click.option('--ota-image-id', required=True, help='ID of the OTA image to get signing keys for')
@click.option('--num-records', type=int, help='Number of records to fetch')
@click.option('--start-id', help='Start ID for pagination')
@click.pass_context
def signing_keys(ctx, ota_image_id: str, num_records: Optional[int],
                start_id: Optional[str]):
    """Get the keys used to sign a specific image"""
    try:
        api_client = ctx.obj['api_client']
        secure_sign_service = SecureSignService(api_client)
        
        result = secure_sign_service.get_signing_keys(
            image_id=ota_image_id,
            num_records=num_records,
            start_id=start_id
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting signing keys: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
