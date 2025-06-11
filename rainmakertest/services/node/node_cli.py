import click
from typing import Optional
import json
import logging
from ...nodes.node_service import NodeService
from ...nodes.node_admin_service import NodeAdminService
from ...nodes.node_sharing_service import NodeSharingService
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

@click.group()
def node():
    """Node management commands"""
    pass

@node.group()
def sharing():
    """Node sharing operations"""
    pass

@sharing.command()
@click.option('--node-id', required=True, help='Node ID to initiate mapping for')
@click.option('--version', default='v1', help='API version')
def initiate_mapping(node_id: str, version: str):
    """Initiate challenge-based node mapping"""
    try:
        api_client = ApiClient()
        sharing_service = NodeSharingService(api_client)
        result = sharing_service.initiate_mapping(node_id, version)
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error initiating mapping: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--request-id', required=True, help='Mapping request ID')
@click.option('--challenge-response', required=True, help='Response to the challenge')
@click.option('--group-id', help='Group ID for the node')
@click.option('--tags', help='Comma-separated list of tags')
@click.option('--metadata', help='JSON string of metadata')
@click.option('--version', default='v1', help='API version')
def verify_mapping(request_id: str, challenge_response: str, group_id: Optional[str], 
                  tags: Optional[str], metadata: Optional[str], version: str):
    """Verify node mapping request"""
    try:
        api_client = ApiClient()
        sharing_service = NodeSharingService(api_client)
        
        tags_list = tags.split(',') if tags else None
        metadata_dict = parse_json_input(metadata)
        
        result = sharing_service.verify_mapping(
            request_id=request_id,
            challenge_response=challenge_response,
            group_id=group_id,
            tags=tags_list,
            metadata=metadata_dict,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error verifying mapping: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--nodes', required=True, help='Comma-separated list of node IDs')
@click.option('--user-name', required=True, help='Username to share with')
@click.option('--primary/--no-primary', default=False, help='Set as primary user')
@click.option('--metadata', help='JSON string of metadata')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def share(ctx, nodes: str, user_name: str, primary: bool, metadata: Optional[str], version: str):
    """Share nodes with another user"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        nodes_list = nodes.split(',')
        metadata_dict = parse_json_input(metadata)
        
        result = sharing_service.share_nodes(
            nodes=nodes_list,
            user_name=user_name,
            primary=primary,
            metadata=metadata_dict,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error sharing nodes: {str(e)}")
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))
        raise click.Abort()

@sharing.command()
@click.option('--nodes', required=True, help='Comma-separated list of node IDs')
@click.option('--user-name', required=True, help='Username to transfer to')
@click.option('--metadata', help='JSON string of metadata')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def transfer(ctx, nodes: str, user_name: str, metadata: Optional[str], version: str):
    """Transfer node ownership to another user"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        nodes_list = nodes.split(',')
        metadata_dict = parse_json_input(metadata)
        
        result = sharing_service.transfer_nodes(
            nodes=nodes_list,
            user_name=user_name,
            metadata=metadata_dict,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error transferring nodes: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--request-id', required=True, help='Share request ID')
@click.option('--accept/--decline', required=True, help='Accept or decline the request')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def respond(ctx, request_id: str, accept: bool, version: str):
    """Respond to a node sharing request"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        result = sharing_service.respond_to_request(
            request_id=request_id,
            accept=accept,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error responding to share request: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--nodes', required=True, help='Comma-separated list of node IDs')
@click.option('--user-name', required=True, help='Username to unshare from')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def unshare(ctx, nodes: str, user_name: str, version: str):
    """Remove node sharing"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        nodes_list = nodes.split(',')
        
        result = sharing_service.unshare_nodes(
            nodes=nodes_list,
            user_name=user_name,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error unsharing nodes: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--node-id', help='Filter by node ID')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def info(ctx, node_id: Optional[str], version: str):
    """Get node sharing information"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        result = sharing_service.get_sharing_info(
            node_id=node_id,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting sharing info: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--request-id', help='Filter by request ID')
@click.option('--primary-user', help='Filter by primary user')
@click.option('--start-request-id', help='Start from this request ID')
@click.option('--version', default='v1', help='API version')
@click.pass_context
def requests(ctx, request_id: Optional[str], primary_user: Optional[str], 
            start_request_id: Optional[str], version: str):
    """Get node sharing requests"""
    try:
        # Use the API client from context which has the correct config_id
        api_client = ctx.obj['api_client']
        sharing_service = NodeSharingService(api_client)
        
        result = sharing_service.get_sharing_requests(
            request_id=request_id,
            primary_user=primary_user,
            start_request_id=start_request_id,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error getting sharing requests: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@sharing.command()
@click.option('--request-id', required=True, help='Request ID to delete')
@click.option('--version', default='v1', help='API version')
def delete_request(request_id: str, version: str):
    """Delete a node sharing request"""
    try:
        api_client = ApiClient()
        sharing_service = NodeSharingService(api_client)
        
        result = sharing_service.delete_sharing_request(
            request_id=request_id,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error deleting sharing request: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@node.group()
def admin():
    """Admin node operations"""
    pass

@admin.command()
@click.option('--node-id', help='Filter by node ID')
@click.option('--node-type', help='Filter by node type')
@click.option('--model', help='Filter by model')
@click.option('--fw-version', help='Filter by firmware version')
@click.option('--subtype', help='Filter by subtype')
@click.option('--project-name', help='Filter by project name')
@click.option('--status', help='Filter by status')
@click.option('--num-records', type=int, help='Number of records to return')
@click.option('--start-id', help='Start from this node ID')
@click.option('--version', default='v1', help='API version')
def list_nodes(node_id: Optional[str], node_type: Optional[str], model: Optional[str],
               fw_version: Optional[str], subtype: Optional[str], project_name: Optional[str],
               status: Optional[str], num_records: Optional[int], start_id: Optional[str],
               version: str):
    """List admin nodes with filtering options"""
    try:
        api_client = ApiClient()
        admin_service = NodeAdminService(api_client)
        
        result = admin_service.get_admin_nodes(
            node_id=node_id,
            node_type=node_type,
            model=model,
            fw_version=fw_version,
            subtype=subtype,
            project_name=project_name,
            status=status,
            num_records=num_records,
            start_id=start_id,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error listing admin nodes: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@admin.command()
@click.option('--node-id', required=True, help='Node ID to update')
@click.option('--metadata', help='JSON string of metadata')
@click.option('--tags', help='Comma-separated list of tags')
@click.option('--version', default='v1', help='API version')
def update_node(node_id: str, metadata: Optional[str], tags: Optional[str], version: str):
    """Update admin node metadata or tags"""
    try:
        api_client = ApiClient()
        admin_service = NodeAdminService(api_client)
        
        metadata_dict = parse_json_input(metadata)
        tags_list = tags.split(',') if tags else None
        
        result = admin_service.update_admin_node(
            node_id=node_id,
            metadata=metadata_dict,
            tags=tags_list,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error updating admin node: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@admin.command()
@click.option('--node-id', required=True, help='Node ID')
@click.option('--tags', required=True, help='Comma-separated list of tags to remove')
@click.option('--version', default='v1', help='API version')
def remove_tags(node_id: str, tags: str, version: str):
    """Remove tags from an admin node"""
    try:
        api_client = ApiClient()
        admin_service = NodeAdminService(api_client)
        
        tags_list = tags.split(',')
        
        result = admin_service.remove_admin_node_tags(
            node_id=node_id,
            tags=tags_list,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        handle_validation_error(e)
    except Exception as e:
        logger.error(f"Error removing admin node tags: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@admin.command()
@click.option('--version', default='v1', help='API version')
def list_tags(version: str):
    """List all tag names used in admin's claimed nodes"""
    try:
        api_client = ApiClient()
        admin_service = NodeAdminService(api_client)
        
        result = admin_service.get_admin_node_tags(version=version)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error listing admin node tags: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@admin.command()
@click.option('--user-name', help='Filter by username')
@click.option('--version', default='v1', help='API version')
def list_user_nodes(user_name: Optional[str], version: str):
    """List user-node associations (admin view)"""
    try:
        api_client = ApiClient()
        admin_service = NodeAdminService(api_client)
        
        result = admin_service.get_admin_user_nodes(
            user_name=user_name,
            version=version
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error listing admin user nodes: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

# Basic node commands
@node.command()
@click.pass_context
def list(ctx):
    """List all nodes"""
    try:
        node_service = ctx.obj['node_service']
        result = node_service.get_user_nodes()
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@node.command()
@click.option('--node-id', help="Node ID to check status")
@click.pass_context
def status(ctx, node_id):
    """Check node status"""
    try:
        node_service = ctx.obj['node_service']
        result = node_service.get_node_status(node_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@node.command()
@click.option('--node-id', help="Node ID to get configuration")
@click.pass_context
def config(ctx, node_id):
    """Get node configuration"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.get_node_config(node_id)
        output = {
            "status": "success",
            "response": result,
            "error": None
        }
        click.echo(json.dumps(output, indent=2))
    except Exception as e:
        output = {
            "status": "error",
            "response": None,
            "error": str(e)
        }
        click.echo(json.dumps(output, indent=2))

@node.command()
@click.option('--node-id', required=True, help="Node ID to update")
@click.option('--tags', required=True, help="Comma-separated tags to add/update")
@click.pass_context
def update(ctx, node_id, tags):
    """Add tags to Node or update the metadata"""
    node_service = ctx.obj['node_service']
    try:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        metadata = {"tags": tag_list}
        result = node_service.update_node_metadata(node_id, metadata)
        output = {
            "status": "success",
            "response": result,
            "error": None
        }
        click.echo(json.dumps(output, indent=2))
    except Exception as e:
        output = {
            "status": "error",
            "response": None,
            "error": str(e)
        }
        click.echo(json.dumps(output, indent=2))

@node.command()
@click.option('--node-id', required=True, help="Node ID to map")
@click.option('--secret-key', required=True, help="Secret key for mapping")
@click.option('--unmap', is_flag=True, help="Unmap instead of map")
@click.pass_context
def map(ctx, node_id, secret_key, unmap):
    """Map or unmap a node"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.map_user_node(node_id, secret_key, "unmap" if unmap else "map")
        output = {
            "status": "success",
            "response": result,
            "error": None
        }
        click.echo(json.dumps(output, indent=2))
    except Exception as e:
        output = {
            "status": "error",
            "response": None,
            "error": str(e)
        }
        click.echo(json.dumps(output, indent=2))

@node.command()
@click.option('--request-id', required=True, help="Request ID from the map operation")
@click.pass_context
def mapping_status(ctx, request_id):
    """Get the status of a node mapping request"""
    try:
        node_service = ctx.obj['node_service']
        result = node_service.get_mapping_status(request_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting mapping status: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@node.command()
@click.option('--node-id', required=True, help="Node ID to delete tags")
@click.option('--tags', required=True, help="Comma-separated tags to delete")
@click.pass_context
def delete_tags(ctx, node_id, tags):
    """Delete node tags"""
    node_service = ctx.obj['node_service']
    try:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        result = node_service.delete_node_tags(node_id, tag_list)
        output = {
            "status": "success",
            "response": result,
            "error": None
        }
        click.echo(json.dumps(output, indent=2))
    except Exception as e:
        output = {
            "status": "error",
            "response": None,
            "error": str(e)
        }
        click.echo(json.dumps(output, indent=2)) 