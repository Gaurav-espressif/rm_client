import click
from typing import Optional, List, Dict
import json
import logging
from ...automation_trigger.automation_trigger import AutomationTriggerService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def automation():
    """Automation trigger operations"""
    pass

def parse_params(params_str: str) -> Dict:
    """Parse params string into dictionary
    Format: key1.subkey1=value1,key2.subkey2=value2
    Example: Light.Brightness=100,Light.Hue=200
    """
    if not params_str:
        return {}
    
    params = {}
    try:
        for param in params_str.split(','):
            if '=' not in param:
                raise ValueError(f"Invalid parameter format: {param}. Expected format: param.subparam=value")
            path, value = param.split('=')
            if '.' not in path:
                raise ValueError(f"Invalid parameter path: {path}. Expected format: param.subparam")
            
            keys = path.split('.')
            
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
            current = params
            for key in keys[:-1]:
                current = current.setdefault(key, {})
            current[keys[-1]] = value
        
        return params
    except Exception as e:
        logger.error(f"Error parsing parameters: {str(e)}")
        raise click.UsageError(
            f"Error parsing parameters: {str(e)}\n"
            f"Example format: Light.Brightness=100,Light.Hue=200\n"
            f"Make sure to quote the entire parameter string if it contains special characters."
        )

def parse_events(events_str: str) -> List[Dict]:
    """Parse events string into list of event dictionaries
    Format: params:check,...
    Example: Light.Brightness=100:==,Light.Hue=200:>
    
    Valid check operators: ==, !=, <, >, <=, >=
    """
    if not events_str:
        return []
    
    events = []
    try:
        for event in events_str.split(','):
            if ':' not in event:
                raise ValueError(f"Invalid event format: {event}. Expected format: param.subparam=value:check")
            params_str, check = event.split(':')
            
            # Validate check operator
            valid_operators = ['==', '!=', '<', '>', '<=', '>=']
            if check not in valid_operators:
                raise ValueError(f"Invalid check operator: {check}. Must be one of: {', '.join(valid_operators)}")
            
            # Parse params
            params = parse_params(params_str)
            if not params:
                raise ValueError(f"Invalid params format: {params_str}. Expected format: param.subparam=value")
            
            events.append({
                "params": params,
                "check": check
            })
        return events
    except Exception as e:
        logger.error(f"Error parsing events: {str(e)}")
        raise click.UsageError(
            f"Error parsing events: {str(e)}\n"
            f"Example format: Light.Brightness=100:==,Light.Hue=200:>\n"
            f"Make sure to quote the entire events string if it contains special characters."
        )

def parse_actions(actions_str: str, node_ids: List[str]) -> List[Dict]:
    """Parse actions string into list of action dictionaries
    Format: params,...
    Example: Light.Output=true,Light.Brightness=100
    """
    if not actions_str:
        return []
    
    actions = []
    params = parse_params(actions_str)
    
    # Create an action for each node ID with the same params
    for node_id in node_ids:
        actions.append({
            "node_id": node_id,
            "params": params
        })
    
    return actions

def parse_location(location_str: str) -> Dict:
    """Parse location string into dictionary
    Format: latitude,longitude
    Example: 18.521428,73.8544541
    """
    if not location_str or ',' not in location_str:
        return {}
    
    lat, lon = location_str.split(',')
    return {
        "latitude": lat.strip(),
        "longitude": lon.strip()
    }

@automation.command()
@click.option('--name', required=True, help='Name of the automation trigger')
@click.option('--event-type', required=True, 
              type=click.Choice(['node_params', 'daylight', 'weather'], case_sensitive=False),
              help='Type of event trigger')
@click.option('--node-id', help='Node ID for node_params event type')
@click.option('--events', required=True, 
              help='Events in format param1.subparam1=value1:check1,param2.subparam2=value2:check2')
@click.option('--actions-node-ids', required=True, multiple=True,
              help='Node IDs to apply actions on (can specify multiple)')
@click.option('--actions', required=True,
              help='Actions in format param1.subparam1=value1,param2.subparam2=value2')
@click.option('--location', help='Location in format latitude,longitude (required for daylight/weather events)')
@click.option('--event-operator', type=click.Choice(['and', 'or'], case_sensitive=False),
              help='Operator to combine multiple events')
@click.option('--metadata', help='Optional metadata as JSON string')
@click.option('--retrigger', is_flag=True, help='Whether to allow retriggering')
@click.pass_context
def create(ctx, name: str, event_type: str, node_id: Optional[str],
           events: str, actions_node_ids: List[str], actions: str,
           location: Optional[str], event_operator: Optional[str],
           metadata: Optional[str], retrigger: bool):
    """Create a new automation trigger"""
    try:
        api_client = ctx.obj['api_client']
        automation_service = AutomationTriggerService(api_client)
        
        # Parse events and actions
        events_list = parse_events(events)
        actions_list = parse_actions(actions, actions_node_ids)
        
        # Parse location if provided
        location_dict = parse_location(location) if location else None
        
        # Parse metadata if provided
        metadata_dict = json.loads(metadata) if metadata else None
        
        result = automation_service.create_automation_trigger(
            name=name,
            event_type=event_type,
            events=events_list,
            actions=actions_list,
            node_id=node_id,
            metadata=metadata_dict,
            location=location_dict,
            event_operator=event_operator,
            retrigger=retrigger
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error creating automation trigger: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@automation.command()
@click.option('--automation-id', required=True, help='ID of the automation trigger to update')
@click.option('--name', help='New name for the automation trigger')
@click.option('--enabled', type=bool, help='Enable/disable the automation trigger')
@click.option('--events', help='Events in format param1.subparam1=value1:check1,param2.subparam2=value2:check2')
@click.option('--actions-node-ids', multiple=True,
              help='Node IDs to apply actions on (can specify multiple)')
@click.option('--actions', help='Actions in format param1.subparam1=value1,param2.subparam2=value2')
@click.option('--event-operator', type=click.Choice(['and', 'or'], case_sensitive=False),
              help='Operator to combine multiple events')
@click.option('--retrigger', type=bool, help='Whether to allow retriggering')
@click.pass_context
def update(ctx, automation_id: str, name: Optional[str], enabled: Optional[bool],
           events: Optional[str], actions_node_ids: Optional[List[str]], 
           actions: Optional[str], event_operator: Optional[str],
           retrigger: Optional[bool]):
    """Update an existing automation trigger"""
    try:
        api_client = ctx.obj['api_client']
        automation_service = AutomationTriggerService(api_client)
        
        # Parse events and actions if provided
        events_list = parse_events(events) if events else None
        actions_list = parse_actions(actions, actions_node_ids) if actions and actions_node_ids else None
        
        result = automation_service.update_automation_trigger(
            automation_id=automation_id,
            name=name,
            enabled=enabled,
            events=events_list,
            actions=actions_list,
            event_operator=event_operator,
            retrigger=retrigger
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error updating automation trigger: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@automation.command()
@click.option('--automation-id', help='ID of specific automation trigger to get')
@click.option('--node-id', help='Get automation triggers for specific node')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', help='Number of records to fetch')
@click.pass_context
def get(ctx, automation_id: Optional[str], node_id: Optional[str],
        start_id: Optional[str], num_records: Optional[str]):
    """Get automation trigger(s)"""
    try:
        api_client = ctx.obj['api_client']
        automation_service = AutomationTriggerService(api_client)
        
        result = automation_service.get_automation_trigger(
            automation_id=automation_id,
            node_id=node_id,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting automation trigger: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@automation.command()
@click.option('--automation-id', required=True, help='ID of the automation trigger to delete')
@click.pass_context
def delete(ctx, automation_id: str):
    """Delete an automation trigger"""
    try:
        api_client = ctx.obj['api_client']
        automation_service = AutomationTriggerService(api_client)
        
        result = automation_service.delete_automation_trigger(automation_id=automation_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error deleting automation trigger: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
