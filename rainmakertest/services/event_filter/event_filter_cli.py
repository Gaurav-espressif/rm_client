import click
from typing import Optional, List
import json
import logging
from ...event_filter.event_filter import EventFilterService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def event_filter():
    """Event filter operations"""
    pass

# Admin Event Filter Operations
@event_filter.group()
def admin():
    """Admin event filter operations"""
    pass

@admin.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID, Node ID, or System entity ID)')
@click.option('--entity-type', required=True, type=click.Choice(['User', 'Node', 'System'], case_sensitive=False),
              help='Entity type')
@click.option('--enabled', required=True, type=bool, help='Whether the event is enabled')
@click.option('--enabled-for-integrations', multiple=True, help='List of integrations to enable')
@click.pass_context
def create(ctx, event_type: str, entity_id: str, entity_type: str,
           enabled: bool, enabled_for_integrations: List[str]):
    """Create a new event filter as admin"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.create_admin_event_filter(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            enabled=enabled,
            enabled_for_integrations=list(enabled_for_integrations) if enabled_for_integrations else None
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error creating admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error creating admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@admin.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID, Node ID, or System entity ID)')
@click.option('--entity-type', required=True, type=click.Choice(['User', 'Node', 'System'], case_sensitive=False),
              help='Entity type')
@click.option('--enabled', required=True, type=bool, help='Whether the event is enabled')
@click.option('--enabled-for-integrations', multiple=True, help='List of integrations to enable')
@click.pass_context
def update(ctx, event_type: str, entity_id: str, entity_type: str,
           enabled: bool, enabled_for_integrations: List[str]):
    """Update an event filter as admin"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.update_admin_event_filter(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            enabled=enabled,
            enabled_for_integrations=list(enabled_for_integrations) if enabled_for_integrations else None
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error updating admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error updating admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@admin.command()
@click.option('--event-type', help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-type', type=click.Choice(['User', 'Node', 'System'], case_sensitive=False),
              help='Entity type')
@click.option('--entity-id', help='Entity ID (User ID, Node ID, or System entity ID)')
@click.pass_context
def get(ctx, event_type: Optional[str], entity_type: Optional[str], entity_id: Optional[str]):
    """Get event filter information as admin"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.get_admin_event_filter(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@admin.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID, Node ID, or System entity ID)')
@click.option('--entity-type', required=True, type=click.Choice(['User', 'Node', 'System'], case_sensitive=False),
              help='Entity type')
@click.pass_context
def delete(ctx, event_type: str, entity_id: str, entity_type: str):
    """Delete an event filter as admin"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.delete_admin_event_filter(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error deleting admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error deleting admin event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

# User Event Filter Operations
@event_filter.group()
def user():
    """User event filter operations"""
    pass

@user.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID or Node ID)')
@click.option('--entity-type', required=True, type=click.Choice(['User', 'Node'], case_sensitive=False),
              help='Entity type')
@click.option('--enabled', required=True, type=bool, help='Whether the event is enabled')
@click.option('--enabled-for-integrations', multiple=True, help='List of integrations to enable')
@click.pass_context
def create(ctx, event_type: str, entity_id: str, entity_type: str,
           enabled: bool, enabled_for_integrations: List[str]):
    """Create a new event filter as user"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.create_user_event_filter(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            enabled=enabled,
            enabled_for_integrations=list(enabled_for_integrations) if enabled_for_integrations else None
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error creating user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error creating user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@user.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID or Node ID)')
@click.option('--entity-type', required=True, type=click.Choice(['User', 'Node'], case_sensitive=False),
              help='Entity type')
@click.option('--enabled', required=True, type=bool, help='Whether the event is enabled')
@click.option('--enabled-for-integrations', multiple=True, help='List of integrations to enable')
@click.pass_context
def update(ctx, event_type: str, entity_id: str, entity_type: str,
           enabled: bool, enabled_for_integrations: List[str]):
    """Update an event filter as user"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.update_user_event_filter(
            event_type=event_type,
            entity_id=entity_id,
            entity_type=entity_type,
            enabled=enabled,
            enabled_for_integrations=list(enabled_for_integrations) if enabled_for_integrations else None
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error updating user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error updating user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@user.command()
@click.option('--event-type', help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-type', type=click.Choice(['User', 'Node'], case_sensitive=False),
              help='Entity type')
@click.option('--entity-id', help='Entity ID (User ID or Node ID)')
@click.pass_context
def get(ctx, event_type: Optional[str], entity_type: Optional[str], entity_id: Optional[str]):
    """Get event filter information as user"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.get_user_event_filter(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@user.command()
@click.option('--event-type', required=True, help='RainMaker event type (e.g. rmaker.event.node_connected)')
@click.option('--entity-id', required=True, help='Entity ID (User ID or Node ID)')
@click.pass_context
def delete(ctx, event_type: str, entity_id: str):
    """Delete an event filter as user"""
    try:
        api_client = ctx.obj['api_client']
        event_filter_service = EventFilterService(api_client)
        
        result = event_filter_service.delete_user_event_filter(
            event_type=event_type,
            entity_id=entity_id
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error deleting user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error deleting user event filter: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
