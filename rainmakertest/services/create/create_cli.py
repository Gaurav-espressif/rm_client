import click
from ...utils.token_json_load import prettify

@click.group()
def create():
    """Create users and admins"""
    pass

@create.command()
@click.option('--user_name', help="Email address or mobile number with country code (e.g. username@domain.com or +1234567890)")
@click.option('--password', help="Password")
@click.option('--locale', default="no_locale", help="Locale preference")
@click.pass_context
def user(ctx, user_name, password, locale):
    """Create a regular user account (email or phone with country code)"""
    if not user_name:
        user_name = click.prompt("Email address or mobile number with country code")
    if not password:
        password = click.prompt("Password", hide_input=True)

    result = ctx.obj['user_service'].create_user(user_name, password)
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