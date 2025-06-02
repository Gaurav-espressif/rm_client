import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...user.user_service import UserService
from ...utils.token_json_load import prettify

@click.group()
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

@click.group()
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
    """Get current user information"""
    result = ctx.obj['user_service'].get_user_info()
    click.echo(f"User info: {prettify(result)}") 