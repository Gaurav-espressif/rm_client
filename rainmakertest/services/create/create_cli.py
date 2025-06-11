import click
import json

@click.group()
def create():
    """Create users and admins"""
    pass

@create.command()
@click.option('--username', help="Email address or mobile number with country code (e.g. username@domain.com or +1234567890)")
@click.option('--password', help="Password")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def user(ctx, username, password, locale):
    """Create a regular user account (email or phone with country code)"""
    if not username:
        username = click.prompt("Email address or mobile number with country code")
    if not password:
        password = click.prompt("Password", hide_input=True)

    result = ctx.obj['user_service'].create_user(username, password)
    click.echo(json.dumps(result, indent=2))

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
    click.echo(json.dumps(result, indent=2))

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
    click.echo(json.dumps(result, indent=2)) 