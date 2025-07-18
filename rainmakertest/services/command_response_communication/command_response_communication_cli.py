import click
from typing import Optional, List, Dict
import json
import logging
from ...command_response_communication.command_response_communication import CommandResponseCommunicationService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def cmd():
    """Command response communication operations"""
    pass

def parse_data(data_str: str) -> Dict:
    """Parse data string into dictionary
    Format: key1=value1,key2=value2
    Example: brightness=10,color=red
    """
    if not data_str:
        return {}
    
    data = {}
    try:
        for item in data_str.split(','):
            if '=' not in item:
                raise ValueError(f"Invalid data format: {item}. Expected format: key=value")
            key, value = item.split('=')
            
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
            
            data[key.strip()] = value
        
        return data
    except Exception as e:
        logger.error(f"Error parsing data: {str(e)}")
        raise click.UsageError(
            f"Error parsing data: {str(e)}\n"
            f"Example format: brightness=10,color=red\n"
            f"Make sure to quote the entire data string if it contains special characters."
        )

# Admin Command Response Operations
@cmd.group()
def admin():
    """Admin command response operations"""
    pass

@admin.command()
@click.option('--node-ids', required=True, multiple=True,
              help='Node IDs to send command to (can specify multiple, max 25)')
@click.option('--cmd', required=True, type=int, 
              help='Command ID (0-65535)')
@click.option('--data', required=True,
              help='Command data in format key1=value1,key2=value2')
@click.option('--is-base64', is_flag=True,
              help='Whether the data is base64 encoded')
@click.option('--timeout', type=int,
              help='Timeout in seconds (default: 30)')
@click.option('--override', type=bool,
              help='Whether to override existing commands')
@click.pass_context
def create(ctx, node_ids: List[str], cmd: int, data: str, 
           is_base64: bool, timeout: Optional[int], override: Optional[bool]):
    """Create a new command response request as admin"""
    try:
        api_client = ctx.obj['api_client']
        cmd_service = CommandResponseCommunicationService(api_client)
        
        # Validate cmd range
        if cmd < 0 or cmd > 65535:
            raise click.UsageError("Command ID must be between 0 and 65535")
        
        # Validate node_ids count
        if len(node_ids) > 25:
            raise click.UsageError("Maximum 25 nodes allowed in a single request")
        
        # Parse data
        data_dict = parse_data(data)
        
        result = cmd_service.create_admin_command_response(
            node_ids=list(node_ids),
            cmd=cmd,
            data=data_dict,
            is_base64=is_base64,
            timeout=timeout,
            override=override
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating admin command response: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@admin.command()
@click.option('--request-id', help='ID of the command response request')
@click.option('--node-id', help='ID of the node')
@click.option('--status', type=click.Choice(['requested', 'in_progress', 'success', 'timed_out', 'failure'], case_sensitive=False),
              help='Status of command')
@click.option('--start-time', type=int, help='Start time of the requests')
@click.option('--end-time', type=int, help='End time of the requests')
@click.option('--cmd-id', type=int, help='Command ID')
@click.option('--desc-order', type=bool, default=True, help='Sort in descending order')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, default=10, help='Number of records to fetch')
@click.pass_context
def get(ctx, request_id: Optional[str], node_id: Optional[str], status: Optional[str],
        start_time: Optional[int], end_time: Optional[int], cmd_id: Optional[int],
        desc_order: bool, start_id: Optional[str], num_records: int):
    """Get command response requests as admin"""
    try:
        api_client = ctx.obj['api_client']
        cmd_service = CommandResponseCommunicationService(api_client)
        
        result = cmd_service.get_admin_command_response(
            request_id=request_id,
            node_id=node_id,
            status=status,
            start_time=start_time,
            end_time=end_time,
            cmd_id=cmd_id,
            desc_order=desc_order,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting admin command response: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

# User Command Response Operations
@cmd.group()
def user():
    """User command response operations"""
    pass

@user.command()
@click.option('--node-ids', required=True, multiple=True,
              help='Node IDs to send command to (can specify multiple, max 25)')
@click.option('--cmd', required=True, type=int, 
              help='Command ID (0-65535)')
@click.option('--data', required=True,
              help='Command data in format key1=value1,key2=value2')
@click.option('--is-base64', is_flag=True,
              help='Whether the data is base64 encoded')
@click.option('--timeout', type=int,
              help='Timeout in seconds (default: 30)')
@click.option('--override', type=bool,
              help='Whether to override existing commands')
@click.pass_context
def create(ctx, node_ids: List[str], cmd: int, data: str, 
           is_base64: bool, timeout: Optional[int], override: Optional[bool]):
    """Create a new command response request as user"""
    try:
        api_client = ctx.obj['api_client']
        cmd_service = CommandResponseCommunicationService(api_client)
        
        # Validate cmd range
        if cmd < 0 or cmd > 65535:
            raise click.UsageError("Command ID must be between 0 and 65535")
        
        # Validate node_ids count
        if len(node_ids) > 25:
            raise click.UsageError("Maximum 25 nodes allowed in a single request")
        
        # Parse data
        data_dict = parse_data(data)
        
        result = cmd_service.create_user_command_response(
            node_ids=list(node_ids),
            cmd=cmd,
            data=data_dict,
            is_base64=is_base64,
            timeout=timeout,
            override=override
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating user command response: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@user.command()
@click.option('--request-id', help='ID of the command response request')
@click.option('--node-id', help='ID of the node')
@click.option('--status', type=click.Choice(['requested', 'in_progress', 'success', 'timed_out', 'failure'], case_sensitive=False),
              help='Status of command')
@click.option('--start-time', type=int, help='Start time of the requests')
@click.option('--end-time', type=int, help='End time of the requests')
@click.option('--cmd-id', type=int, help='Command ID')
@click.option('--desc-order', type=bool, default=True, help='Sort in descending order')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, default=10, help='Number of records to fetch')
@click.pass_context
def get(ctx, request_id: Optional[str], node_id: Optional[str], status: Optional[str],
        start_time: Optional[int], end_time: Optional[int], cmd_id: Optional[int],
        desc_order: bool, start_id: Optional[str], num_records: int):
    """Get command response requests as user"""
    try:
        api_client = ctx.obj['api_client']
        cmd_service = CommandResponseCommunicationService(api_client)
        
        result = cmd_service.get_user_command_response(
            request_id=request_id,
            node_id=node_id,
            status=status,
            start_time=start_time,
            end_time=end_time,
            cmd_id=cmd_id,
            desc_order=desc_order,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting user command response: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
