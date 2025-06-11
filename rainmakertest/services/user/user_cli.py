import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...user.user_service import UserService
from ...utils.token_json_load import prettify
import json

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
    click.echo(json.dumps(result, indent=2))

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
    click.echo(json.dumps(result, indent=2))

@user.command()
@click.option('--name', help="Update user's name (e.g., --name 'John Doe')")
@click.option('--phone', help="Update user's phone number (e.g., --phone '+1234567890')")
@click.option('--verify-code', help="Verification code for phone number (e.g., --verify-code '123456')")
@click.option('--mfa/--no-mfa', help="Enable/disable Multi-Factor Authentication (e.g., --mfa or --no-mfa)")
@click.option('--locale', help="Update user's locale (e.g., --locale 'en')")
@click.pass_context
def update(ctx, name, phone, verify_code, mfa, locale):
    """Update user details including name, phone number, MFA status, and locale.
    
    Examples:
        Update name: rmcli user update --name "John Doe"
        Update phone: rmcli user update --phone "+1234567890"
        Verify phone: rmcli user update --phone "+1234567890" --verify-code "123456"
        Toggle MFA: rmcli user update --mfa
        Update locale: rmcli user update --locale "en"
    """
    user_service = ctx.obj['user_service']
    result = user_service.update_user_details(
        name=name,
        phone_number=phone,
        verification_code=verify_code,
        mfa=mfa,
        locale=locale
    )
    click.echo(result)

@user.command()
@click.option('--username', required=True, help="Username (email/phone) for login")
@click.option('--password', help="Password for login (e.g., --password 'pass123')")
@click.option('--verify-code', help="Verification code for MFA (e.g., --verify-code '123456')")
@click.option('--session', help="Session token for MFA verification (e.g., --session 'session_token')")
@click.option('--refresh-token', help="Refresh token to extend session (e.g., --refresh-token 'token')")
@click.pass_context
def login(ctx, username, password, verify_code, session, refresh_token):
    """Login with various authentication methods.
    
    Examples:
        Password login: rmcli user login --username "user@example.com" --password "pass123"
        MFA verification: rmcli user login --username "user@example.com" --verify-code "123456" --session "session_token"
        Extend session: rmcli user login --refresh-token "token"
    """
    user_service = ctx.obj['user_service']
    result = user_service.login(
        user_name=username,
        password=password,
        verification_code=verify_code,
        session=session,
        refresh_token=refresh_token
    )
    click.echo(result)

@user.command()
@click.option('--current', required=True, help="Current password")
@click.option('--new', required=True, help="New password")
@click.pass_context
def change_password(ctx, current, new):
    """Change user password"""
    user_service = ctx.obj['user_service']
    result = user_service.change_password(current, new)
    click.echo(result)

@user.command()
@click.option('--username', required=True, help="Username (email/phone) for password reset")
@click.option('--new-password', help="New password for reset (e.g., --new-password 'newpass')")
@click.option('--verify-code', help="Verification code for reset (e.g., --verify-code '123456')")
@click.pass_context
def forgot_password(ctx, username, new_password, verify_code):
    """Handle forgot password flow.
    
    Examples:
        Start reset: rmcli user forgot-password --username "user@example.com"
        Complete reset: rmcli user forgot-password --username "user@example.com" --new-password "newpass" --verify-code "123456"
    """
    user_service = ctx.obj['user_service']
    result = user_service.forgot_password(
        user_name=username,
        password=new_password,
        verification_code=verify_code
    )
    click.echo(result)

@user.command()
@click.pass_context
def info(ctx):
    """Get current user's information"""
    user_service = ctx.obj['user_service']
    result = user_service.get_user_info()
    click.echo(json.dumps(result, indent=2))

@user.command()
@click.option('--verify-code', help="Verification code received via email")
@click.option('--request', is_flag=True, help="Request account deletion and receive verification code")
@click.pass_context
def delete(ctx, verify_code, request):
    """Delete user account
    
    This is a two-step process:
    1. First run with --request to initiate deletion and receive verification code via email
    2. Then run with --verify-code to complete deletion using the code received
    
    Examples:
        Request deletion: rmcli user delete --request
        Complete deletion: rmcli user delete --verify-code "123456"
    """
    user_service = ctx.obj['user_service']
    
    if request:
        click.echo("Initiating account deletion request...")
        result = user_service.delete_user(request=True)
        if result.get("status") == "success":
            click.echo("✓ Verification code has been sent to your email")
            click.echo("Please check your email and run the command again with --verify-code")
        else:
            click.echo(f"Error: {result.get('description', 'Unknown error')}")
    elif verify_code:
        click.echo("Completing account deletion...")
        result = user_service.delete_user(verification_code=verify_code)
        if result.get("status") == "success":
            click.echo("✓ Account successfully deleted")
        else:
            click.echo(f"Error: {result.get('description', 'Unknown error')}")
    else:
        click.echo("Error: Either --request or --verify-code must be provided")
        click.echo("Run 'rmcli user delete --help' for usage information") 