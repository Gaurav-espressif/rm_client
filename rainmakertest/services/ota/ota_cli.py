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
                output = {
                    "status": "error",
                    "response": None,
                    "error": "No firmware file provided and default switch.bin not found"
                }
                click.echo(json.dumps(output, indent=2))
                return

        result = ota_service.upload_image(
            image_name=name,
            fw_version=version,
            model=model,
            type=type,
            base64_fwimage=base64_fwimage,
            bin_file_path=bin_file_path
        )
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

@image.command()
@click.pass_context
def list(ctx):
    """List all OTA images"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.get_images()
        if result.get('ota_images'):
            headers = ['Image ID', 'Name', 'Type', 'Version', 'Model', 'Size', 'Uploaded']
            table_data = [
                [
                    img['ota_image_id'],
                    img['image_name'],
                    img['type'],
                    img['fw_version'],
                    img['model'],
                    f"{img['file_size'] / 1024:.2f} KB",
                    img['upload_timestamp']
                ]
                for img in result['ota_images']
            ]
            output = {
                "status": "success",
                "response": {
                    "headers": headers,
                    "data": table_data
                },
                "error": None
            }
        else:
            output = {
                "status": "success",
                "response": [],
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

@image.command()
@click.option('--image-id', help="Image ID to delete")
@click.pass_context
def delete(ctx, image_id):
    """Delete an OTA image"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.delete_image(image_id)
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

@image.command()
@click.option('--image-id', help="Image ID to archive/unarchive")
@click.option('--unarchive', is_flag=True, help="Unarchive instead of archive")
@click.pass_context
def archive(ctx, image_id, unarchive):
    """Archive or unarchive an OTA image"""
    ota_service = ctx.obj['ota_image_service']
    try:
        result = ota_service.archive_image(image_id, unarchive)
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
                "status": "success",
                "response": {
                    "headers": headers,
                    "data": table_data
                },
                "error": None
            }
        else:
            output = {
                "status": "success",
                "response": [],
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
        click.echo(json.dumps({
            "status": "failure",
            "description": str(e),
            "error_code": 500
        }, indent=2))

@job.command()
@click.option('--job-id', help="Job ID to check status")
@click.pass_context
def status(ctx, job_id):
    """Check OTA job status"""
    ota_job_service = ctx.obj['ota_job_service']
    try:
        result = ota_job_service.get_job_status(job_id)
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