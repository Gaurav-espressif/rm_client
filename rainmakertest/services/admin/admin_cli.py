import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...admin.admin_user_service import AdminUserService
from ...utils.token_json_load import prettify

@click.group()
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
    """List users with admin privileges"""
    admin_service = ctx.obj['admin_service']
    result = admin_service.list_users(
        username=username,
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
    """Update user with admin privileges"""
    admin_service = ctx.obj['admin_service']
    result = admin_service.update_user(
        username=username,
        quota=quota,
        admin=admin,
        superadmin=superadmin
    )
    click.echo(f"User updated: {prettify(result)}")

@admin.command()
@click.option('--username', help="Username to delete")
@click.pass_context
def delete_user(ctx, username):
    """Delete user with admin privileges"""
    admin_service = ctx.obj['admin_service']
    result = admin_service.delete_user(username)
    click.echo(f"User deleted: {prettify(result)}")

@click.group()
def create():
    """Create different types of users"""
    pass

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