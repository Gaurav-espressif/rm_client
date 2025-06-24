import click
from typing import Optional
import json
import logging
from ...device_grouping.grouping import GroupingService
from ...utils.api_client import ApiClient
from json.decoder import JSONDecodeError

logger = logging.getLogger(__name__)

def handle_validation_error(error: ValueError) -> None:
    """Handle validation errors consistently"""
    logger.error(f"Validation error: {str(error)}")
    click.echo(json.dumps({
        "status": "failure",
        "description": str(error),
        "error_code": 400
    }, indent=2))
    raise click.Abort()

def parse_json_input(json_str: Optional[str]) -> Optional[dict]:
    """Safely parse JSON input"""
    if not json_str:
        return None
    try:
        return json.loads(json_str)
    except JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": f"Invalid JSON input - {str(e)}",
            "error_code": 400
        }, indent=2))
        raise click.Abort()

def parse_list_input(list_str: Optional[str]) -> Optional[list]:
    """Parse comma-separated list input"""
    if not list_str:
        return None
    return [item.strip() for item in list_str.split(',')]

@click.group()
def grouping():
    """Device grouping management commands"""
    pass

# Admin Group Operations
@grouping.group()
def admin():
    """Admin device group operations"""
    pass

@admin.command()
@click.option('--group-name', required=True, help='Group name')
@click.option('--parent-group-id', help='Parent group ID')
@click.option('--nodes', help='Comma-separated list of node IDs')
@click.option('--description', help='Group description')
@click.option('--type', help='Group type')
@click.option('--node-fw-version', help='Node firmware version')
@click.option('--node-model', help='Node model')
@click.option('--node-type', help='Node type')
@click.option('--group-metadata', help='JSON string of group metadata')
@click.option('--custom-data', help='JSON string of custom data')
@click.pass_context
def create(ctx, group_name: str, parent_group_id: Optional[str], nodes: Optional[str],
           description: Optional[str], type: Optional[str], node_fw_version: Optional[str],
           node_model: Optional[str], node_type: Optional[str], group_metadata: Optional[str],
           custom_data: Optional[str]):
    """Create admin device group"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        nodes_list = parse_list_input(nodes)
        metadata_dict = parse_json_input(group_metadata)
        custom_data_dict = parse_json_input(custom_data)
        
        result = grouping_service.create_admin_group(
            group_name=group_name,
            parent_group_id=parent_group_id,
            nodes=nodes_list,
            description=description,
            group_type=type,
            node_fw_version=node_fw_version,
            node_model=node_model,
            node_type=node_type,
            group_metadata=metadata_dict,
            custom_data=custom_data_dict
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error creating admin group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@admin.command()
@click.option('--group-id', required=True, help='Group ID to update')
@click.option('--group-name', help='New group name')
@click.option('--type', help='Group type')
@click.option('--operation', help='Operation: add or remove')
@click.option('--nodes', help='Comma-separated list of node IDs')
@click.option('--description', help='Group description')
@click.option('--group-metadata', help='JSON string of group metadata')
@click.option('--custom-data', help='JSON string of custom data')
@click.option('--regroup', is_flag=True, help='Regroup based on query')
@click.pass_context
def update(ctx, group_id: str, group_name: Optional[str], type: Optional[str],
           operation: Optional[str], nodes: Optional[str], description: Optional[str],
           group_metadata: Optional[str], custom_data: Optional[str], regroup: bool):
    """Update admin device group"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        nodes_list = parse_list_input(nodes)
        metadata_dict = parse_json_input(group_metadata)
        custom_data_dict = parse_json_input(custom_data)
        
        result = grouping_service.update_admin_group(
            group_id=group_id,
            group_name=group_name,
            group_type=type,
            operation=operation,
            nodes=nodes_list,
            description=description,
            group_metadata=metadata_dict,
            custom_data=custom_data_dict,
            regroup=regroup
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error updating admin group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@admin.command()
@click.option('--group-id', help='Group ID to get')
@click.option('--group-name', help='Group name to get')
@click.option('--node-details', is_flag=True, help='Include node details')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return')
@click.option('--node-model', help='Filter by node model')
@click.option('--node-type', help='Filter by node type')
@click.option('--node-fw-version', help='Filter by node firmware version')
@click.pass_context
def get(ctx, group_id: Optional[str], group_name: Optional[str], node_details: bool,
        start_id: Optional[str], num_records: Optional[int], node_model: Optional[str],
        node_type: Optional[str], node_fw_version: Optional[str]):
    """Get admin device group details"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.get_admin_group(
            group_id=group_id,
            group_name=group_name,
            node_details=node_details,
            start_id=start_id,
            num_records=num_records,
            node_model=node_model,
            node_type=node_type,
            node_fw_version=node_fw_version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting admin group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@admin.command()
@click.option('--group-id', required=True, help='Group ID to delete')
@click.pass_context
def delete(ctx, group_id: str):
    """Delete admin device group"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.delete_admin_group(group_id)
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error deleting admin group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

# User Group Operations
@grouping.group()
def user():
    """User device group operations"""
    pass

@user.command()
@click.option('--group-name', required=True, help='Group name')
@click.option('--parent-group-id', help='Parent group ID')
@click.option('--nodes', help='Comma-separated list of node IDs')
@click.option('--description', help='Group description')
@click.option('--group-metadata', help='JSON string of group metadata')
@click.option('--type', help='Group type')
@click.option('--mutually-exclusive', is_flag=True, help='Make group mutually exclusive')
@click.option('--custom-data', help='JSON string of custom data')
@click.option('--is-matter', is_flag=True, help='Create as matter fabric')
@click.pass_context
def create(ctx, group_name: str, parent_group_id: Optional[str], nodes: Optional[str],
           description: Optional[str], group_metadata: Optional[str], type: Optional[str],
           mutually_exclusive: bool, custom_data: Optional[str], is_matter: bool):
    """Create user device group or matter fabric"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        nodes_list = parse_list_input(nodes)
        metadata_dict = parse_json_input(group_metadata)
        custom_data_dict = parse_json_input(custom_data)
        
        result = grouping_service.create_user_group(
            group_name=group_name,
            parent_group_id=parent_group_id,
            nodes=nodes_list,
            description=description,
            group_metadata=metadata_dict,
            group_type=type,
            mutually_exclusive=mutually_exclusive,
            custom_data=custom_data_dict,
            is_matter=is_matter
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error creating user group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@user.command()
@click.option('--group-id', help='Group ID to update')
@click.option('--group-name', help='New group name')
@click.option('--operation', help='Operation: add or remove')
@click.option('--type', help='Group type')
@click.option('--mutually-exclusive', is_flag=True, help='Set mutually exclusive')
@click.option('--nodes', help='Comma-separated list of node IDs')
@click.option('--description', help='Group description')
@click.option('--group-metadata', help='JSON string of group metadata')
@click.option('--custom-data', help='JSON string of custom data')
@click.option('--matter-controller', help='Matter controller flag')
@click.pass_context
def update(ctx, group_id: Optional[str], group_name: Optional[str], operation: Optional[str],
           type: Optional[str], mutually_exclusive: bool, nodes: Optional[str],
           description: Optional[str], group_metadata: Optional[str], custom_data: Optional[str],
           matter_controller: Optional[str]):
    """Update user device group or matter fabric"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        nodes_list = parse_list_input(nodes)
        metadata_dict = parse_json_input(group_metadata)
        custom_data_dict = parse_json_input(custom_data)
        
        result = grouping_service.update_user_group(
            group_id=group_id,
            group_name=group_name,
            operation=operation,
            group_type=type,
            mutually_exclusive=mutually_exclusive if mutually_exclusive else None,
            nodes=nodes_list,
            description=description,
            group_metadata=metadata_dict,
            custom_data=custom_data_dict,
            matter_controller=matter_controller
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error updating user group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@user.command()
@click.option('--group-id', help='Group ID to get')
@click.option('--group-name', help='Group name to get')
@click.option('--node-list', is_flag=True, help='Include node list')
@click.option('--sub-groups', is_flag=True, help='Include sub groups')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return')
@click.option('--node-details', is_flag=True, help='Include node details')
@click.option('--matter-node-list', is_flag=True, help='Include matter node list')
@click.option('--is-matter', is_flag=True, help='Get matter fabrics')
@click.option('--fabric-details', is_flag=True, help='Include fabric details')
@click.pass_context
def get(ctx, group_id: Optional[str], group_name: Optional[str], node_list: bool,
        sub_groups: bool, start_id: Optional[str], num_records: Optional[int],
        node_details: bool, matter_node_list: bool, is_matter: bool, fabric_details: bool):
    """Get user device group details"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.get_user_group(
            group_id=group_id,
            group_name=group_name,
            node_list=node_list,
            sub_groups=sub_groups,
            start_id=start_id,
            num_records=num_records,
            node_details=node_details,
            matter_node_list=matter_node_list,
            is_matter=is_matter,
            fabric_details=fabric_details
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting user group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@user.command()
@click.option('--group-id', required=True, help='Group ID to delete')
@click.option('--leave', is_flag=True, help='Leave the group')
@click.option('--remove-sharing', is_flag=True, help='Remove sharing')
@click.option('--user-name', help='Username to remove sharing from')
@click.pass_context
def delete(ctx, group_id: str, leave: bool, remove_sharing: bool, user_name: Optional[str]):
    """Delete user device group or matter fabric"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.delete_user_group(
            group_id=group_id,
            leave=leave,
            remove_sharing=remove_sharing,
            user_name=user_name
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error deleting user group: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

# Group Sharing Operations
@user.group()
def sharing():
    """Group sharing operations"""
    pass

@sharing.command()
@click.option('--groups', required=True, help='Comma-separated list of group IDs')
@click.option('--user-name', required=True, help='Username to share with')
@click.option('--primary', is_flag=True, help='Set as primary user')
@click.option('--metadata', help='JSON string of metadata')
@click.pass_context
def share(ctx, groups: str, user_name: str, primary: bool, metadata: Optional[str]):
    """Share groups with another user"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        groups_list = parse_list_input(groups)
        metadata_dict = parse_json_input(metadata)
        
        result = grouping_service.share_group(
            groups=groups_list,
            user_name=user_name,
            primary=primary,
            metadata=metadata_dict
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error sharing groups: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@sharing.command()
@click.option('--group-id', help='Group ID to get sharing info for')
@click.option('--sub-groups', is_flag=True, help='Include sub groups')
@click.option('--metadata', is_flag=True, help='Include metadata')
@click.option('--parent-groups', is_flag=True, help='Include parent groups')
@click.pass_context
def info(ctx, group_id: Optional[str], sub_groups: bool, metadata: bool, parent_groups: bool):
    """Get group sharing information"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.get_group_sharing(
            group_id=group_id,
            sub_groups=sub_groups,
            metadata=metadata,
            parent_groups=parent_groups
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting sharing info: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@sharing.command()
@click.option('--request-id', help='Request ID to get')
@click.option('--primary-user', help='Primary user flag')
@click.option('--start-request-id', help='Start request ID for pagination')
@click.option('--start-user-name', help='Start username for pagination')
@click.option('--num-records', type=int, help='Number of records to return')
@click.pass_context
def requests(ctx, request_id: Optional[str], primary_user: Optional[str],
             start_request_id: Optional[str], start_user_name: Optional[str],
             num_records: Optional[int]):
    """Get group sharing requests"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.get_sharing_requests(
            request_id=request_id,
            primary_user=primary_user,
            start_request_id=start_request_id,
            start_user_name=start_user_name,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting sharing requests: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@sharing.command()
@click.option('--request-id', required=True, help='Request ID to delete')
@click.pass_context
def delete_request(ctx, request_id: str):
    """Delete group sharing request"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.delete_sharing_request(request_id)
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error deleting sharing request: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@sharing.command()
@click.option('--request-id', required=True, help='Request ID to respond to')
@click.option('--accept/--decline', required=True, help='Accept or decline the request')
@click.pass_context
def respond(ctx, request_id: str, accept: bool):
    """Respond to group sharing request"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.respond_to_sharing_request(
            request_id=request_id,
            accept=accept
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error responding to sharing request: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@user.command()
@click.pass_context
def node_acl(ctx):
    """Get fabric Node ACLs"""
    try:
        api_client = ctx.obj['api_client']
        grouping_service = GroupingService(api_client)
        
        result = grouping_service.get_node_acl()
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting node ACL: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()
