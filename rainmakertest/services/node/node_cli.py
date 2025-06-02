import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...nodes.node_service import NodeService
import json

@click.group()
@click.pass_context
def node(ctx):
    """Node operations"""
    pass

@node.command()
@click.pass_context
def list(ctx):
    """List all nodes"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.get_user_nodes()
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        output = {
            "status": "error",
            "response": None,
            "error": str(e)
        }
        click.echo(json.dumps(output, indent=2))

@node.command()
@click.option('--node-id', help="Node ID to check status")
@click.pass_context
def status(ctx, node_id):
    """Check node status"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.get_node_status(node_id)
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
@click.option('--node-id', help="Node ID to map")
@click.option('--unmap', is_flag=True, help="Unmap instead of map")
@click.pass_context
def map(ctx, node_id, unmap):
    """Map or unmap a node"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.map_node(node_id, unmap)
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
@click.option('--node-id', required=True, help="Node ID to check mapping status")
@click.option('--request-id', required=True, help="Request ID from the map operation")
@click.pass_context
def mapping_status(ctx, node_id, request_id):
    """Check the status of a node mapping request"""
    node_service = ctx.obj['node_service']
    try:
        result = node_service.get_mapping_status(node_id, request_id)
        click.echo(json.dumps({
            "status": "success",
            "response": result,
            "error": None
        }, indent=2))
    except Exception as e:
        click.echo(json.dumps({
            "status": "error",
            "response": None,
            "error": str(e)
        }, indent=2))
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