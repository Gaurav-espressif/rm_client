import click
from typing import Optional
from ...utils.api_client import ApiClient
from ...utils.email_service import EmailService

@click.group()
def email():
    """Email operations"""
    pass

@email.command()
@click.pass_context
def generate(ctx):
    """Generate a new random email address"""
    email_service = EmailService()
    email_address = email_service.generate_random_email()
    click.echo(f"Email address generated: {email_address}")

@email.command()
@click.option('--email', help="Email address to verify (uses last generated if not specified)")
@click.pass_context
def verify(ctx, email):
    """Verify an email address by retrieving the verification code"""
    email_service = EmailService()
    
    if not email:
        # Try to get the last generated email
        try:
            email = email_service.get_last_generated_email()
        except Exception as e:
            click.echo("No email specified and no previously generated email found")
            return
    
    click.echo(f"Checking verification code for {email}...")
    result = email_service.get_verification_code(email)
    if result:
        click.echo(f"Verification code: {result}")
    else:
        click.echo("No verification code found in emails") 
