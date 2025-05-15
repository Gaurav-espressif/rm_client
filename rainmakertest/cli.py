import os

import click
from typing import Optional, List
from .utils.api_client import ApiClient
from .auth.login_service import LoginService
from .user.user_service import UserService
from .admin.admin_user_service import AdminUserService
from .ota.ota_image_service import OTAService
from .ota.ota_job_service import OTAJobService
from .utils.token_json_load import prettify
from .nodes.node_service import NodeService
from .nodes.node_admin_service import NodeAdminService
from tabulate import tabulate

@click.group()
@click.pass_context
def cli(ctx):
    """Rainmaker CLI Tool"""
    ctx.ensure_object(dict)
    api_client = ApiClient()
    ctx.obj['api_client'] = api_client
    ctx.obj['login_service'] = LoginService(api_client)
    ctx.obj['user_service'] = UserService(api_client)
    ctx.obj['admin_service'] = AdminUserService(api_client)
    ctx.obj['ota_image_service'] = OTAService(api_client)
    ctx.obj['ota_job_service'] = OTAJobService(api_client)
    ctx.obj['node_service'] = NodeService(api_client)
    ctx.obj['node_admin_service'] = NodeAdminService(api_client)


# Login commands
@cli.group()
def login():
    """Login operations"""
    pass


@login.command()
@click.option('--username', prompt=True, help="Username (email or phone)")
@click.option('--password', prompt=True, hide_input=True, help="User password")
@click.pass_context
def user(ctx, username, password):
    """Login as regular user"""
    result = ctx.obj['login_service'].login_user(username, password)
    click.echo(f"Login successful. Access token: {result['token']['access_token'][:15]}...")

# Logout command
@cli.command()
@click.pass_context
def logout(ctx):
    """Logout current user by clearing tokens"""
    try:
        ctx.obj['api_client'].clear_token()
        click.echo("✓ Successfully logged out")
    except Exception as e:
        click.echo(f"✗ Logout failed: {str(e)}")


# User commands
@cli.group()
def user():
    """User operations"""
    pass


@user.command()
@click.option('--username', prompt=True, help="Username (email or phone)")
@click.option('--password', prompt=True, hide_input=True, help="Password")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def create(ctx, username, password, locale):
    """Create a new user"""
    result = ctx.obj['user_service'].create_user(username, password, locale)
    click.echo(f"User created: {result}")


@user.command()
@click.option('--username', prompt=True, help="Username used during signup")
@click.option('--verification-code', prompt=True, help="Verification code received via email/SMS")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def confirm(ctx, username, verification_code, locale):
    """Confirm a new user account with verification code"""
    result = ctx.obj['user_service'].confirm_user(
        username=username,
        verification_code=verification_code,
        locale=locale
    )
    click.echo(f"User confirmed: {prettify(result)}")


@user.command()
@click.pass_context
def info(ctx):
    """Get current user info"""
    result = ctx.obj['user_service'].get_user_info()
    click.echo(f"User info: {prettify(result)}")


# Admin commands
@cli.group()
def admin():
    """Admin operations"""
    pass


@admin.command()
@click.option('--username', prompt=True, help="Admin username (email)")
@click.option('--super', is_flag=True, help="Create as superadmin")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def create_user(ctx, username, super, locale):
    """Create an admin user"""
    result = ctx.obj['admin_service'].create_admin_user(
        username,
        super_admin=super,
        locale=locale
    )
    click.echo(f"Admin user created: {prettify(result)}")


# OTA Image commands
@cli.group()
def ota():
    """OTA operations"""
    pass


@ota.group()
def image():
    """OTA Image operations"""
    pass


@image.command()
@click.option('--base64', help="Base64 encoded firmware image (optional if default .bin exists)")
@click.option('--file', type=click.Path(exists=True), help="Path to .bin firmware file (optional)")
@click.option('--name', required=True, help="Image name")
@click.option('--version', help="Firmware version")
@click.option('--model', help="Device model")
@click.option('--type', help="Device type")
@click.pass_context
def upload(ctx, base64, file, name, version, model, type):
    """Upload a new OTA image (uses switch.bin if no --base64 or --file provided)"""
    ota_service = ctx.obj['ota_image_service']

    # Default file path (adjust based on your project structure)
    DEFAULT_BIN = os.path.join(os.path.dirname(__file__), '..', 'switch.bin')

    try:
        if file:
            # Handle .bin file upload
            result = ota_service.upload_image(
                bin_file_path=file,
                image_name=name,
                fw_version=version,
                model=model,
                type=type
            )
        elif base64:
            # Handle direct base64 upload
            result = ota_service.upload_image(
                base64_fwimage=base64,
                image_name=name,
                fw_version=version,
                model=model,
                type=type
            )
        else:
            # Fallback to default switch.bin
            if os.path.exists(DEFAULT_BIN):
                click.echo("No firmware provided - using default switch.bin")
                result = ota_service.upload_image(
                    bin_file_path=DEFAULT_BIN,
                    image_name=name,
                    fw_version=version,
                    model=model,
                    type=type
                )
            else:
                raise click.UsageError(
                    "No firmware provided and default switch.bin not found.\n"
                    "Please use either --base64, --file, or place switch.bin in the project root."
                )

        click.echo(f"Image uploaded: {prettify(result)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@image.command()
@click.option('--image-id', help="Specific image ID to fetch")
@click.option('--image-name', help="Image name to search")
@click.option('--contains', is_flag=True, help="Enable pattern search")
@click.pass_context
def list(ctx, image_id, image_name, contains):
    """List OTA images"""
    result = ctx.obj['ota_image_service'].get_images(
        ota_image_id=image_id,
        ota_image_name=image_name,
        contains=contains
    )
    click.echo(f"OTA Images: {prettify(result)}")


@image.command()
@click.option('--image-id', prompt=True, help="Image ID to delete")
@click.pass_context
def delete(ctx, image_id):
    """Delete an OTA image"""
    result = ctx.obj['ota_image_service'].delete_image(image_id)
    click.echo(f"Image deleted: {prettify(result)}")


@image.command()
@click.option('--image-id', prompt=True, help="Image ID to archive/unarchive")
@click.option('--unarchive', is_flag=True, help="Unarchive instead of archive")
@click.pass_context
def archive(ctx, image_id, unarchive):
    """Archive or unarchive an OTA image"""
    result = ctx.obj['ota_image_service'].archive_image(
        ota_image_id=image_id,
        archive=not unarchive
    )
    click.echo(f"Image {'unarchived' if unarchive else 'archived'}: {prettify(result)}")


# OTA Job commands
@ota.group()
def job():
    """OTA Job operations"""
    pass


@job.command()
@click.option('--name', prompt=True, help="OTA job name")
@click.option('--image-id', prompt=True, help="OTA image ID")
@click.option('--description', default="Default OTA job description", help="Job description")
@click.option('--nodes', help="Node IDs (comma-separated for multiple nodes)")
@click.option('--priority', type=int, default=5, help="Job priority (1-10, default:5)")
@click.option('--timeout', type=int, default=1296000, help="Job timeout in seconds (default:15 days)")
@click.option('--force', is_flag=True, help="Force push OTA")
@click.option('--approval', is_flag=True, help="Require user approval")
@click.option('--notify', is_flag=True, help="Notify end users")
@click.option('--continuous', is_flag=True, help="Keep job active after completion")
@click.option('--serialized', is_flag=True, help="Network serialized delivery")
@click.pass_context
def create(ctx, name, image_id, description, nodes, priority, timeout,
           force, approval, notify, continuous, serialized):
    """Create a new OTA job"""
    # Convert comma-separated nodes to list if provided
    node_list = nodes.split(',') if nodes else None

    result = ctx.obj['ota_job_service'].create_job(
        ota_job_name=name,
        ota_image_id=image_id,
        description=description,
        nodes=node_list,
        priority=priority,
        timeout=timeout,
        force_push=force,
        user_approval=approval,
        notify=notify,
        continuous=continuous,
        network_serialised=serialized,
    )
    click.echo(f"OTA Job created: {prettify(result)}")


@job.command()
@click.option('--job-id', help="Specific job ID to fetch")
@click.option('--job-name', help="Job name to search")
@click.option('--image-id', help="Filter by image ID")
@click.option('--archived', is_flag=True, help="Show archived jobs")
@click.option('--all', is_flag=True, help="Show all jobs")
@click.pass_context
def list(ctx, job_id, job_name, image_id, archived, all):
    """List OTA jobs"""
    result = ctx.obj['ota_job_service'].get_jobs(
        ota_job_id=job_id,
        ota_job_name=job_name,
        ota_image_id=image_id,
        archived=archived,
        all=all
    )
    click.echo(f"OTA Jobs: {prettify(result)}")


@job.command()
@click.option('--job-id', prompt=True, help="Job ID to update")
@click.option('--archive', is_flag=True, help="Archive instead of cancel")
@click.pass_context
def update(ctx, job_id, archive):
    """Cancel or archive an OTA job"""
    result = ctx.obj['ota_job_service'].update_job(
        ota_job_id=job_id,
        archive=archive
    )
    action = "archived" if archive else "cancelled"
    click.echo(f"Job {action}: {prettify(result)}")


@job.command()
@click.option('--job-id', prompt=True, help="Job ID to check status")
@click.pass_context
def status(ctx, job_id):
    """Get OTA job status"""
    result = ctx.obj['ota_job_service'].get_job_status(job_id)
    click.echo(f"Job status: {prettify(result)}")


# Node commands
@cli.group()
def node():
    """Node management commands"""
    pass


@node.command(name="list")
@click.pass_context
def list_nodes(ctx):
    """List all nodes associated with the user"""
    try:
        nodes = ctx.obj['node_service'].get_user_nodes()
        if not nodes:
            click.echo("No nodes found")
            return

        # Format output as a table

        table = []
        for node in nodes:
            table.append([
                node.get('node_id', 'N/A'),
                node.get('name', 'N/A'),
                node.get('type', 'N/A'),
                node.get('status', 'N/A')
            ])

        click.echo(tabulate(
            table,
            headers=["Node ID", "Name", "Type", "Status"],
            tablefmt="grid"
        ))
    except Exception as e:
        click.echo(f"Error listing nodes: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to configure")
@click.option('--tags', multiple=True, help="Tags to add/update")
@click.option('--metadata', type=click.Path(exists=True), help="JSON file containing metadata")
@click.pass_context
def update(ctx, node_id, tags, metadata):
    """Update node metadata and/or tags"""
    try:
        metadata_dict = {}
        if metadata:
            import json
            with open(metadata) as f:
                metadata_dict = json.load(f)

        result = ctx.obj['node_service'].update_node_metadata(
            node_id=node_id,
            tags=list(tags) if tags else None,
            metadata=metadata_dict if metadata_dict else None
        )
        click.echo(f"Successfully updated node {node_id}")
    except Exception as e:
        click.echo(f"Error updating node: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to modify")
@click.option('--tags', multiple=True, required=True, help="Tags to remove")
@click.pass_context
def delete_tags(ctx, node_id, tags):
    """Remove tags from a node"""
    try:
        result = ctx.obj['node_service'].delete_node_tags(
            node_id=node_id,
            tags=list(tags)
        )
        click.echo(f"Successfully removed tags from node {node_id}")
    except Exception as e:
        click.echo(f"Error removing tags: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to query")
@click.pass_context
def config(ctx, node_id):
    """Get node configuration"""
    try:
        config = ctx.obj['node_service'].get_node_config(node_id)
        import json
        click.echo(json.dumps(config, indent=2))
    except Exception as e:
        click.echo(f"Error getting config: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to check")
@click.pass_context
def status(ctx, node_id):
    """Get node online/offline status"""
    try:
        status = ctx.obj['node_service'].get_node_status(node_id)
        click.echo(f"Node {node_id} status: {status.get('status', 'unknown')}")
    except Exception as e:
        click.echo(f"Error getting status: {str(e)}", err=True)


# Node admin commands
@node.group()
def admin():
    """Admin node management"""
    pass


@admin.command(name="list")
@click.option('--node-id', help="Filter by specific node ID")
@click.option('--type', help="Filter by node type")
@click.option('--model', help="Filter by model")
@click.option('--fw-version', help="Filter by firmware version")
@click.option('--subtype', help="Filter by subtype")
@click.option('--project-name', help="Filter by project name")
@click.option('--status', help="Filter by status (online/offline)")
@click.option('--num-records', type=int, help="Number of records to return")
@click.option('--start-id', help="Starting ID for pagination")
@click.pass_context
def admin_list_nodes(ctx, **filters):
    """List nodes with admin privileges (supports filtering)"""
    try:
        # Remove None values from filters
        filters = {k: v for k, v in filters.items() if v is not None}
        nodes = ctx.obj['node_admin_service'].get_admin_nodes(**filters)

        if not nodes:
            click.echo("No nodes found matching criteria")
            return

        from tabulate import tabulate
        table = []
        for node in nodes:
            table.append([
                node.get('node_id', 'N/A'),
                node.get('type', 'N/A'),
                node.get('model', 'N/A'),
                node.get('fw_version', 'N/A'),
                node.get('status', 'N/A')
            ])

        click.echo(tabulate(
            table,
            headers=["Node ID", "Type", "Model", "Firmware", "Status"],
            tablefmt="grid"
        ))
    except Exception as e:
        click.echo(f"Error listing admin nodes: {str(e)}", err=True)


if __name__ == '__main__':
    cli()