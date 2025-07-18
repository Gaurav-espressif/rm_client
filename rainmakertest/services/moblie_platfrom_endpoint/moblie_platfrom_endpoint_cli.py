import click
import json
import logging
from ...moblie_platfrom_endpoint.moblie_platfrom_endpoint import MobilePlatformEndpointService

logger = logging.getLogger(__name__)

@click.group()
def mobile_platform():
    """Mobile platform endpoint operations"""
    pass

@mobile_platform.command()
@click.option('--platform', required=True, help='Platform type (GCM, APNS, or APNS_SANDBOX)')
@click.option('--mobile-device-token', required=True, help='Mobile device token')
@click.option('--platform-type', required=True, help='Platform type (e.g., huawei)')
@click.pass_context
def create(ctx, platform: str, mobile_device_token: str, platform_type: str):
    """Create a new platform endpoint for mobile device"""
    try:
        api_client = ctx.obj['api_client']
        service = MobilePlatformEndpointService(api_client)
        
        result = service.create_platform_endpoint(
            platform=platform,
            mobile_device_token=mobile_device_token,
            platform_type=platform_type
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating platform endpoint: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@mobile_platform.command()
@click.pass_context
def get(ctx):
    """Get configured platform endpoints"""
    try:
        api_client = ctx.obj['api_client']
        service = MobilePlatformEndpointService(api_client)
        
        result = service.get_platform_endpoints()
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting platform endpoints: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@mobile_platform.command()
@click.option('--mobile-device-token', help='Mobile device token')
@click.option('--endpoint', help='Platform endpoint ARN')
@click.pass_context
def delete(ctx, mobile_device_token: str, endpoint: str):
    """Delete a configured platform endpoint"""
    if not mobile_device_token and not endpoint:
        click.echo("Error: Either --mobile-device-token or --endpoint must be specified")
        raise click.Abort()
        
    try:
        api_client = ctx.obj['api_client']
        service = MobilePlatformEndpointService(api_client)
        
        result = service.delete_platform_endpoint(
            mobile_device_token=mobile_device_token,
            endpoint=endpoint
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error deleting platform endpoint: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
