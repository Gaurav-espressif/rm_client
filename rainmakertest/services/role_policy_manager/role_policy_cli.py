import click
from typing import Optional, List
import json
import logging
from ...role_policy_manager.role_policy import RolePolicyService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def role_policy():
    """Role and policy management operations"""
    pass

# Policy Operations
@role_policy.group()
def policy():
    """Policy operations"""
    pass

@policy.command()
@click.option('--policy-name', required=True, help='Name of the policy')
@click.option('--policy-json', required=True, type=str, help='Policy JSON as a string')
@click.pass_context
def create(ctx, policy_name: str, policy_json: str):
    """Create a new policy"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Parse policy JSON from string
        try:
            policy_json_dict = json.loads(policy_json)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {str(e)}")
            click.echo("Invalid JSON format for policy_json")
            raise click.Abort()
        
        result = role_policy_service.create_policy(
            policy_name=policy_name,
            policy_json=policy_json_dict
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error creating policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error creating policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@policy.command()
@click.option('--policy-name', required=True, help='Name of the policy to update')
@click.option('--policy-json', required=True, type=str, help='Updated policy JSON as a string')
@click.pass_context
def update(ctx, policy_name: str, policy_json: str):
    """Update an existing policy"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Parse policy JSON from string
        try:
            policy_json_dict = json.loads(policy_json)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {str(e)}")
            click.echo("Invalid JSON format for policy_json")
            raise click.Abort()
        
        result = role_policy_service.update_policy(
            policy_name=policy_name,
            policy_json=policy_json_dict
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error updating policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error updating policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@policy.command()
@click.option('--policy-name', help='Name of the policy to get (optional)')
@click.pass_context
def get(ctx, policy_name: Optional[str]):
    """Get policy information"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        result = role_policy_service.get_policy(
            policy_name=policy_name
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@policy.command()
@click.option('--policy-name', required=True, help='Name of the policy to delete')
@click.pass_context
def delete(ctx, policy_name: str):
    """Delete a policy"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        result = role_policy_service.delete_policy(
            policy_name=policy_name
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error deleting policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error deleting policy: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

# Role Operations
@role_policy.group()
def role():
    """Role operations"""
    pass

@role.command()
@click.option('--role-name', required=True, help='Name of the role')
@click.option('--policies', required=True, help='Comma-separated list of policy names')
@click.option('--role-level', required=True, type=int, help='Role level (0 is highest)')
@click.pass_context
def create(ctx, role_name: str, policies: str, role_level: int):
    """Create a new role"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Split policies string into list
        policy_list = [p.strip() for p in policies.split(',')]
        
        result = role_policy_service.create_role(
            role_name=role_name,
            policies=policy_list,
            role_level=role_level
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error creating role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@role.command()
@click.option('--role-name', required=True, help='Name of the role to update')
@click.option('--operation', required=True, type=click.Choice(['add', 'remove']), help='Operation to perform')
@click.option('--policies', required=True, help='Comma-separated list of policy names')
@click.option('--role-level', type=int, help='New role level (optional)')
@click.pass_context
def update(ctx, role_name: str, operation: str, policies: str, role_level: Optional[int]):
    """Update an existing role"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Split policies string into list
        policy_list = [p.strip() for p in policies.split(',')]
        
        result = role_policy_service.update_role(
            role_name=role_name,
            operation=operation,
            policies=policy_list,
            role_level=role_level
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error updating role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error updating role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@role.command()
@click.option('--role-name', help='Name of the role to get (optional)')
@click.pass_context
def get(ctx, role_name: Optional[str]):
    """Get role information"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        result = role_policy_service.get_role(
            role_name=role_name
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@role.command()
@click.option('--role-name', required=True, help='Name of the role to delete')
@click.pass_context
def delete(ctx, role_name: str):
    """Delete a role"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        result = role_policy_service.delete_role(
            role_name=role_name
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error deleting role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error deleting role: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

# RBAC Deployment Settings Operations
@role_policy.group()
def deployment():
    """RBAC deployment settings operations"""
    pass

@deployment.command()
@click.option('--service', default='rbac', 
              type=click.Choice(['cognito_appclient', 'rbac', 'encryption', 'user_archival', 'node_apis', 
                               'custom_user_context', 'location_trigger', 'mobile_app', 'oauth_only', 'custom_sms']),
              help='Service whose configuration is to be fetched (default: rbac)')
@click.option('--platform', 
              type=click.Choice(['ios', 'android']),
              help='Platform (required if service is mobile_app)')
@click.option('--package-name', 
              help='Package name (required if service is mobile_app)')
@click.option('--is-email-user-pool', 
              type=click.BOOL, default=False,
              help='Use true for older/email-only userPool or false for newer/email-and-phone userPool')
@click.pass_context
def get(ctx, service: str, platform: Optional[str], package_name: Optional[str], is_email_user_pool: bool):
    """Get deployment settings for a service"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Validate mobile_app requirements
        if service == 'mobile_app':
            if not platform:
                raise click.UsageError("Platform is required when service is mobile_app")
            if not package_name:
                raise click.UsageError("Package name is required when service is mobile_app")
        
        result = role_policy_service.get_deployment_settings(
            service=service,
            platform=platform,
            package_name=package_name,
            is_email_user_pool=is_email_user_pool
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting deployment settings: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@deployment.command()
@click.option('--service', default='rbac',
              type=click.Choice(['rbac', 'node_apis', 'custom_user_context', 'location_trigger', 
                               'encryption', 'user_archival', 'oauth_only', 'cmd_resp_history', 
                               'custom_sms', 'node_data_access', 'ota_network_serialisation_degree']),
              help='Service to configure (default: rbac)')
@click.option('--rbac-enabled', 
              type=click.BOOL,
              help='Enable/disable RBAC (for rbac service)')
@click.option('--node-apis-enabled',
              type=click.BOOL,
              help='Enable/disable Node APIs (for node_apis service)')
@click.option('--custom-user-context-enabled',
              type=click.BOOL,
              help='Enable/disable custom user context (for custom_user_context service)')
@click.option('--encryption-enabled',
              type=click.BOOL,
              help='Enable/disable encryption (for encryption service)')
@click.option('--user-archival-enabled',
              type=click.BOOL,
              help='Enable/disable user archival (for user_archival service)')
@click.option('--oauth-only-enabled',
              type=click.BOOL,
              help='Enable/disable OAuth only (for oauth_only service)')
@click.option('--cmd-resp-history-enabled',
              type=click.BOOL,
              help='Enable/disable command response history (for cmd_resp_history service)')
@click.option('--ota-network-serialisation-degree',
              type=int,
              help='OTA network serialisation degree (for ota_network_serialisation_degree service)')
@click.pass_context
def update(ctx, service: str, rbac_enabled: Optional[bool], node_apis_enabled: Optional[bool],
           custom_user_context_enabled: Optional[bool], encryption_enabled: Optional[bool],
           user_archival_enabled: Optional[bool], oauth_only_enabled: Optional[bool],
           cmd_resp_history_enabled: Optional[bool], ota_network_serialisation_degree: Optional[int]):
    """Update deployment settings for a service"""
    try:
        api_client = ctx.obj['api_client']
        role_policy_service = RolePolicyService(api_client)
        
        # Build kwargs based on service
        kwargs = {}
        if service == 'rbac' and rbac_enabled is not None:
            kwargs['rbac_enabled'] = rbac_enabled
        elif service == 'node_apis' and node_apis_enabled is not None:
            kwargs['node_apis_enabled'] = node_apis_enabled
        elif service == 'custom_user_context' and custom_user_context_enabled is not None:
            kwargs['custom_user_context_enabled'] = custom_user_context_enabled
        elif service == 'encryption' and encryption_enabled is not None:
            kwargs['encryption_enabled'] = encryption_enabled
        elif service == 'user_archival' and user_archival_enabled is not None:
            kwargs['user_archival_enabled'] = user_archival_enabled
        elif service == 'oauth_only' and oauth_only_enabled is not None:
            kwargs['oauth_only_enabled'] = oauth_only_enabled
        elif service == 'cmd_resp_history' and cmd_resp_history_enabled is not None:
            kwargs['cmd_resp_history_enabled'] = cmd_resp_history_enabled
        elif service == 'ota_network_serialisation_degree' and ota_network_serialisation_degree is not None:
            kwargs['ota_network_serialisation_degree'] = ota_network_serialisation_degree
        
        # Validate that at least one parameter is provided
        if not kwargs:
            raise click.UsageError(f"No configuration parameter provided for service '{service}'")
        
        result = role_policy_service.update_deployment_settings(
            service=service,
            **kwargs
        )
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error updating deployment settings: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
