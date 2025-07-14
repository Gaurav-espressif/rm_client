import click
from typing import Optional, List, Dict
import json
import logging
from ...node_parameter_operations.node_parameter_operations import NodeParameterOperationsService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def params():
    """Node parameter operations"""
    pass

def parse_params(params_str: str) -> Dict:
    """Parse params string into dictionary
    Format: service.param=value,service.param2=value2
    Example: Light.brightness=100,Light.output=true
    """
    if not params_str:
        return {}
    
    params = {}
    try:
        for param in params_str.split(','):
            if '=' not in param:
                raise ValueError(f"Invalid parameter format: {param}. Expected format: service.param=value")
            path, value = param.split('=')
            if '.' not in path:
                raise ValueError(f"Invalid parameter path: {path}. Expected format: service.param")
            
            service, param_name = path.split('.')
            
            # Convert value to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Keep as string
            
            # Build nested dictionary
            if service not in params:
                params[service] = {}
            params[service][param_name] = value
        
        return params
    except Exception as e:
        logger.error(f"Error parsing parameters: {str(e)}")
        raise click.UsageError(
            f"Error parsing parameters: {str(e)}\n"
            f"Example format: Light.brightness=100,Light.output=true\n"
            f"Make sure to quote the entire parameter string if it contains special characters."
        )

@params.command()
@click.option('--node-id', help='Node ID (can be provided here or in the params)')
@click.option('--params', required=True, multiple=True,
              help='Parameters in format service.param=value,service.param2=value2. Use multiple times for multiple nodes.')
@click.option('--params-node-ids', help='Space-separated list of node IDs corresponding to each --params option. Required if --node-id is not provided.')
@click.pass_context
def update(ctx, node_id: Optional[str], params: List[str], params_node_ids: Optional[str]):
    """Update node parameters"""
    try:
        api_client = ctx.obj['api_client']
        params_service = NodeParameterOperationsService(api_client)
        
        # Build params list based on input format
        params_list = []
        
        if node_id:
            # Single node update via query parameter
            if len(params) > 1:
                raise click.UsageError("Only one --params allowed when using --node-id")
            params_list = [{
                "payload": parse_params(params[0])
            }]
        else:
            # Multiple nodes or node_id in payload
            if not params_node_ids:
                raise click.UsageError("Either --node-id or --params-node-ids must be provided")
            
            # Split space-separated node IDs
            node_ids = params_node_ids.split()
            if len(params) != len(node_ids):
                raise click.UsageError(f"Number of --params ({len(params)}) must match number of node IDs ({len(node_ids)})")
            
            # For multiple nodes, include node_id in each payload
            for node_id, param_str in zip(node_ids, params):
                params_list.append({
                    "node_id": node_id,
                    "payload": parse_params(param_str)
                })
        
        # For multiple nodes, don't pass node_id as query parameter
        result = params_service.update_node_params(
            params_list=params_list,
            node_id=node_id if len(params_list) == 1 else None
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error updating node parameters: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@params.command()
@click.option('--node-id', required=True, help='Node ID to get parameters for')
@click.pass_context
def get(ctx, node_id: str):
    """Get node parameters"""
    try:
        api_client = ctx.obj['api_client']
        params_service = NodeParameterOperationsService(api_client)
        
        result = params_service.get_node_params(node_id=node_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting node parameters: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
