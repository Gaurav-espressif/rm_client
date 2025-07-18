import click
from typing import Optional, List, Dict
import json
import logging
from ...external_api_passthrough.external_api_passthrough import ExternalApiPassthroughService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def passthrough():
    """External API passthrough operations"""
    pass

@passthrough.command()
@click.option('--service-id', help='Service ID to fetch specific service')
@click.option('--service-name', help='Service name prefix to filter services')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, default=30, help='Number of records to fetch (max 30)')
@click.pass_context
def config(ctx, service_id: Optional[str], service_name: Optional[str],
           start_id: Optional[str], num_records: int):
    """Fetches external API configurations"""
    try:
        api_client = ctx.obj['api_client']
        passthrough_service = ExternalApiPassthroughService(api_client)
        
        result = passthrough_service.get_passthrough_config(
            service_id=service_id,
            service_name=service_name,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting passthrough config: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@passthrough.command()
@click.option('--service-id', required=True, help='Service ID to call')
@click.option('--query-params', help='JSON string of query parameters')
@click.option('--headers', help='JSON string of headers')
@click.option('--path-params', help='Path parameters string')
@click.pass_context
def get(ctx, service_id: str, query_params: Optional[str], 
        headers: Optional[str], path_params: Optional[str]):
    """Retrieves data from external API via GET request"""
    try:
        api_client = ctx.obj['api_client']
        passthrough_service = ExternalApiPassthroughService(api_client)
        
        result = passthrough_service.get_passthrough_data(
            service_id=service_id,
            query_params_json=query_params,
            headers_json=headers,
            path_params_string=path_params
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting passthrough data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@passthrough.command()
@click.option('--service-id', required=True, help='Service ID to call')
@click.option('--query-params', help='JSON string of query parameters')
@click.option('--headers', help='JSON string of headers')
@click.option('--path-params', help='Path parameters string')
@click.option('--body', help='JSON string for request body')
@click.pass_context
def post(ctx, service_id: str, query_params: Optional[str], 
         headers: Optional[str], path_params: Optional[str], body: Optional[str]):
    """Makes a POST request to an external API endpoint"""
    try:
        api_client = ctx.obj['api_client']
        passthrough_service = ExternalApiPassthroughService(api_client)
        
        result = passthrough_service.post_passthrough_data(
            service_id=service_id,
            query_params_json=query_params,
            headers_json=headers,
            path_params_string=path_params,
            body_json=body
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error posting passthrough data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
