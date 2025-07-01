import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...ota.ota_image_service import OTAService
from ...ota.ota_job_service import OTAJobService
from tabulate import tabulate
import base64
import json

@click.group()
@click.pass_context
def ota(ctx):
    """OTA operations"""
    pass

@ota.group()
def image():
    """OTA image operations"""
    pass

@image.command()
@click.option('--base64-str', help="Base64 encoded firmware image (optional if default .bin exists)")
@click.option('--file', type=click.Path(exists=True), help="Path to .bin firmware file (optional)")
@click.option('--name', required=True, help="Image name")
@click.option('--version', help="Firmware version")
@click.option('--model', help="Device model")
@click.option('--type', help="Device type")
@click.pass_context
def upload(ctx, base64_str, file, name, version, model, type):
    """Upload a new OTA image"""
    ota_service = ctx.obj['ota_image_service']
    
    try:
        # Handle base64 input
        if base64_str:
            base64_fwimage = base64_str
            bin_file_path = None
        # Handle file input
        elif file:
            bin_file_path = file
            base64_fwimage = None
        else:
            # Try to use default switch.bin
            try:
                with open('switch.bin', 'rb') as f:
                    base64_fwimage = base64.b64encode(f.read()).decode('utf-8')
                bin_file_path = None
            except FileNotFoundError:
                click.echo(json.dumps("No firmware file provided and default switch.bin not found", indent=2))
                return

        result = ota_service.upload_image(
            image_name=name,
            fw_version=version,
            model=model,
            type=type,
            base64_fwimage=base64_fwimage,
            bin_file_path=bin_file_path
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@image.command()
@click.option('--image-id', help="OTA Image ID")
@click.option('--name', help="OTA Image Name")
@click.option('--type', help="OTA Image Type")
@click.option('--model', help="OTA Image Model")
@click.option('--num-records', help="Number of records to fetch (for pagination)")
@click.option('--start-id', help="Start ID of records to fetch (for pagination)")
@click.option('--contains', is_flag=True, help="Enable pattern search on image name")
@click.option('--archived', is_flag=True, help="Show only archived OTA images")
@click.option('--all', is_flag=True, help="Show all images regardless of archive status")
@click.pass_context
def list(ctx, image_id, name, type, model, num_records, start_id, contains, archived, all):
    """List all OTA images"""
    ota_service = ctx.obj['ota_image_service']
    try:
        # Extract parameters
        params = {
            'ota_image_id': image_id,
            'ota_image_name': name,
            'type': type,
            'model': model,
            'num_records': num_records,
            'start_id': start_id,
            'contains': contains,
            'archived': archived,
            'all': all
        }
        
        # Remove None values to only pass provided parameters
        params = {k: v for k, v in params.items() if v is not None}
        
        result = ota_service.get_images(**params)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@image.command()
@click.option('--image-id', help="Image ID to delete")
@click.pass_context
def delete(ctx, image_id):
    """Delete an OTA image"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.delete_image(image_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@image.command()
@click.option('--image-id', help="Image ID to archive/unarchive")
@click.option('--unarchive', is_flag=True, help="Unarchive instead of archive")
@click.pass_context
def archive(ctx, image_id, unarchive):
    """Archive or unarchive an OTA image"""
    ota_service = ctx.obj['ota_image_service']
    try:
        # If --unarchive flag is True, we want to unarchive (archive=False)
        # If --unarchive flag is False (default), we want to archive (archive=True)
        result = ota_service.archive_image(image_id, not unarchive)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@image.command()
@click.option('--file-name', required=True, help="Name of the file with file extension")
@click.pass_context
def get_upload_url(ctx, file_name):
    """Get pre-signed URL for firmware package upload"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.get_package_upload_url(file_name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@image.command()
@click.option('--name', required=True, help="Image name")
@click.option('--type', required=True, help="Image type (e.g. alexa)")
@click.option('--file-path', required=True, help="Path to the file that has been uploaded to S3")
@click.pass_context
def upload_package(ctx, name, type, file_path):
    """Upload a new firmware package that was previously uploaded to S3"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.upload_package(name, type, file_path)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@ota.group()
def job():
    """OTA job operations"""
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
    ota_job_service = ctx.obj['ota_job_service']

    try:
        # Convert comma-separated nodes string to list
        node_list = nodes.split(',') if nodes else []
        
        result = ota_job_service.create_job(
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
            network_serialised=serialized
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@job.command()
@click.pass_context
def list(ctx):
    """List OTA jobs"""
    ota_job_service = ctx.obj['ota_job_service']
    try:
        result = ota_job_service.get_jobs()
        if result.get('otaJobs'):
            headers = ['Job ID', 'Name', 'Image ID', 'Status', 'Triggered', 'Completed', 'Failed']
            table_data = [
                [
                    job['ota_job_id'],
                    job['ota_job_name'],
                    job['ota_image_id'],
                    job['status'],
                    job['triggered_timestamp'],
                    job['completed_count'],
                    job['failed_count']
                ]
                for job in result['otaJobs']
            ]
            output = {
                "headers": headers,
                "data": table_data
            }
        else:
            output = []
        click.echo(json.dumps(output, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@job.command()
@click.option('--job-id', help="Job ID to update")
@click.option('--archive', is_flag=True, help="Archive instead of cancel")
@click.pass_context
def update(ctx, job_id, archive):
    """Update an OTA job"""
    ota_job_service = ctx.obj['ota_job_service']
    try:
        result = ota_job_service.update_job(job_id, archive)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@job.command()
@click.option('--job-id', help="Job ID to check status")
@click.pass_context
def status(ctx, job_id):
    """Check OTA job status"""
    ota_job_service = ctx.obj['ota_job_service']
    try:
        result = ota_job_service.get_job_status(job_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2))

@job.command()
@click.option('--job-id', required=True, help="OTA Job ID")
@click.pass_context
def summary(ctx, job_id):
    """Get summary of OTA job status including node counts"""
    ota_job_service = ctx.obj['ota_job_service']
    try:
        result = ota_job_service.get_job_status_summary(job_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps(str(e), indent=2)) 