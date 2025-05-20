import os
import click
from typing import Optional, List

from rainmakertest.utils.email_service import EmailService
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
import logging
import json


@click.group()
@click.option('--debug', is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx, debug):
    """Rainmaker CLI Tool"""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

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
@click.option('--username', help="Username (email or phone)")
@click.option('--password', help="User password")
@click.pass_context
def user(ctx, username, password):
    """Login as regular user"""
    if not username:
        username = click.prompt("Username")
    if not password:
        password = click.prompt("Password", hide_input=True)

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
def create():
    """Create different types of users"""
    pass


@create.command()
@click.option('--username', help="Username (email or phone)")
@click.option('--password', help="Password")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def user(ctx, username, password, locale):
    """Create a regular user account"""
    if not username:
        username = click.prompt("Username")
    if not password:
        password = click.prompt("Password", hide_input=True)

    result = ctx.obj['user_service'].create_user(username, password)
    click.echo(f"User created: {result}")


@create.command()
@click.option('--username', help="Admin username (email)")
@click.option('--quota', type=int, help="Admin quota")
@click.pass_context
def admin(ctx, username, quota):
    """Create an admin user account"""
    if not username:
        username = click.prompt("Username")
    if quota is None:
        quota = click.prompt("Quota", type=int)

    result = ctx.obj['admin_service'].create_admin(
        user_name=username,
        quota=quota
    )
    click.echo(f"Admin user created: {prettify(result)}")


@create.command()
@click.option('--username', help="Superadmin username (email)")
@click.pass_context
def superadmin(ctx, username):
    """Create a superadmin user account"""
    if not username:
        username = click.prompt("Username")

    result = ctx.obj['admin_service'].create_superadmin(
        user_name=username
    )
    click.echo(f"Superadmin user created: {prettify(result)}")


# User commands
@cli.group()
def user():
    """User operations"""
    pass


@user.command()
@click.option('--username', help="Username used during signup")
@click.option('--verification-code', help="Verification code received via email/SMS")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def confirm(ctx, username, verification_code, locale):
    """Confirm a new user account with verification code"""
    if not username:
        username = click.prompt("Username")
    if not verification_code:
        verification_code = click.prompt("Verification code")

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
@click.option('--username', help="Filter by username")
@click.option('--all-users', is_flag=True, help="Get all users")
@click.option('--admin', is_flag=True, help="Filter admin users")
@click.option('--superadmin', is_flag=True, help="Filter superadmin users")
@click.pass_context
def list_users(ctx, username, all_users, admin, superadmin):
    """List users with optional filters"""
    result = ctx.obj['admin_service'].get_user_details(
        user_name=username,
        all_users=all_users,
        admin=admin,
        superadmin=superadmin
    )
    click.echo(f"Users: {prettify(result)}")


@admin.command()
@click.option('--username', help="Username to update")
@click.option('--quota', type=int, help="New quota value")
@click.option('--admin', is_flag=True, help="Set as admin")
@click.option('--superadmin', is_flag=True, help="Set as superadmin")
@click.pass_context
def update_user(ctx, username, quota, admin, superadmin):
    """Update user details"""
    if not username:
        username = click.prompt("Username")

    payload = {}
    if quota is not None:
        payload['quota'] = quota
    if admin:
        payload['admin'] = True
    if superadmin:
        payload['super_admin'] = True

    result = ctx.obj['admin_service'].update_admin_user(
        user_name=username,
        payload=payload
    )
    click.echo(f"User updated: {prettify(result)}")


@admin.command()
@click.option('--username', help="Username to delete")
@click.pass_context
def delete_user(ctx, username):
    """Delete a user account"""
    if not username:
        username = click.prompt("Username")

    result = ctx.obj['admin_service'].delete_admin_user(user_name=username)
    click.echo(f"User deleted: {prettify(result)}")


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
    DEFAULT_BIN = os.path.join(os.path.dirname(__file__), '..', 'switch.bin')

    try:
        if file:
            result = ota_service.upload_image(
                bin_file_path=file,
                image_name=name,
                fw_version=version,
                model=model,
                type=type
            )
        elif base64:
            result = ota_service.upload_image(
                base64_fwimage=base64,
                image_name=name,
                fw_version=version,
                model=model,
                type=type
            )
        else:
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
@click.option('--image-id', help="Image ID to delete")
@click.pass_context
def delete(ctx, image_id):
    """Delete an OTA image"""
    if not image_id:
        image_id = click.prompt("Image ID")

    result = ctx.obj['ota_image_service'].delete_image(image_id)
    click.echo(f"Image deleted: {prettify(result)}")


@image.command()
@click.option('--image-id', help="Image ID to archive/unarchive")
@click.option('--unarchive', is_flag=True, help="Unarchive instead of archive")
@click.pass_context
def archive(ctx, image_id, unarchive):
    """Archive or unarchive an OTA image"""
    if not image_id:
        image_id = click.prompt("Image ID")

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
@click.option('--name', help="OTA job name")
@click.option('--image-id', help="OTA image ID")
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
    if not name:
        name = click.prompt("Job name")
    if not image_id:
        image_id = click.prompt("Image ID")

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
@click.option('--job-id', help="Job ID to update")
@click.option('--archive', is_flag=True, help="Archive instead of cancel")
@click.pass_context
def update(ctx, job_id, archive):
    """Cancel or archive an OTA job"""
    if not job_id:
        job_id = click.prompt("Job ID")

    result = ctx.obj['ota_job_service'].update_job(
        ota_job_id=job_id,
        archive=archive
    )
    action = "archived" if archive else "cancelled"
    click.echo(f"Job {action}: {prettify(result)}")


@job.command()
@click.option('--job-id', help="Job ID to check status")
@click.pass_context
def status(ctx, job_id):
    """Get OTA job status"""
    if not job_id:
        job_id = click.prompt("Job ID")

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
        response = ctx.obj['node_service'].get_user_nodes(raw=True)
        click.echo(json.dumps(response, indent=4))
    except Exception as e:
        click.echo(f"Error listing nodes: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to query")
@click.pass_context
def config(ctx, node_id):
    """Get node configuration"""
    try:
        config = ctx.obj['node_service'].get_node_config(node_id)
        if not config:
            click.echo(f"No configuration found for node {node_id}")
            return

        click.echo(json.dumps(config, indent=2))
    except Exception as e:
        click.echo(f"Error getting config: {str(e)}", err=True)


@node.command()
@click.option('--node-id', required=True, help="Node ID to check")
@click.pass_context
def status(ctx, node_id):
    """Get node online/offline status"""
    try:
        status_info = ctx.obj['node_service'].get_node_status(node_id)
        status = status_info.get('status', 'unknown')
        click.echo(f"Node {node_id} status: {status}")
    except Exception as e:
        click.echo(f"Error getting status: {str(e)}", err=True)


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
@click.option('--node-id', required=True, help="Node ID to map/unmap")
@click.option('--secret-key', required=True, help="Secret key for the node")
@click.option('--operation', type=click.Choice(['map', 'unmap']), required=True, help="Operation to perform")
@click.pass_context
def map(ctx, node_id, secret_key, operation):
    """Map or unmap a node to the user"""
    try:
        result = ctx.obj['node_service'].map_user_node(
            node_id=node_id,
            secret_key=secret_key,
            operation=operation
        )
        request_id = result.get('request_id')
        if request_id:
            click.echo(f"Mapping operation initiated. Request ID: {request_id}")
            click.echo("Use 'node mapping-status --request-id <id>' to check status")
        else:
            click.echo(f"Operation completed: {prettify(result)}")
    except Exception as e:
        click.echo(f"Error mapping node: {str(e)}", err=True)


@node.command()
@click.option('--request-id', required=True, help="Request ID from mapping operation")
@click.pass_context
def mapping_status(ctx, request_id):
    """Check status of a node mapping request"""
    try:
        status = ctx.obj['node_service'].get_mapping_status(request_id)
        click.echo(f"Mapping status: {prettify(status)}")
    except Exception as e:
        click.echo(f"Error getting mapping status: {str(e)}", err=True)


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
        filters = {k: v for k, v in filters.items() if v is not None}
        nodes = ctx.obj['node_admin_service'].get_admin_nodes(**filters)

        if not nodes:
            click.echo("No nodes found matching criteria")
            return

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


@cli.group()
def email():
    """Email operations for testing"""
    pass


@email.command()
@click.pass_context
def generate(ctx):
    """Generate a random test email address"""
    try:
        email_service = EmailService()
        random_email = email_service.generate_random_email()
        click.echo(f"Generated email: {random_email}")
        ctx.obj['last_generated_email'] = random_email
    except Exception as e:
        click.echo(f"Error generating email: {str(e)}", err=True)
        raise click.Abort()


@email.command()
@click.option('--email', help="Email address to verify (uses last generated if not specified)")
@click.pass_context
def verify(ctx, email):
    """Verify an email address by retrieving the verification code"""
    try:
        email_service = EmailService()
        email_to_verify = email or ctx.obj.get('last_generated_email')
        if not email_to_verify:
            raise click.UsageError("No email specified and no last generated email found")

        click.echo(f"Checking verification code for {email_to_verify}...")

        code = email_service.get_verification_code(email_to_verify)
        if code:
            click.echo(f"Verification code: {code}")
        else:
            click.echo("No verification code found in emails", err=True)
    except Exception as e:
        click.echo(f"Error verifying email: {str(e)}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()