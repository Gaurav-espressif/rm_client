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
    """Generate a new email address
    
    This command requires Mailosaur configuration. Please set the following environment variables:
    1. MAILOSAUR_API_KEY: Your Mailosaur API key
    2. MAILOSAUR_SERVER_ID: Your Mailosaur server ID
    3. MAILOSAUR_SERVER_DOMAIN: Your Mailosaur server domain
    
    You can get these values from your Mailosaur account at https://mailosaur.com/app/servers
    """
    try:
        email_service = EmailService()
        email_address = email_service.generate_random_email()
        click.echo(f"Generated email address: {email_address}")
    except ValueError as e:
        click.echo(str(e), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error generating email address: {str(e)}", err=True)
        raise click.Abort()

@email.command()
@click.option('--email', help="Email address to verify (uses last generated if not specified)")
@click.pass_context
def verify(ctx, email):
    """Verify an email address by retrieving the verification code
    
    This command requires Mailosaur configuration. Please set the following environment variables:
    1. MAILOSAUR_API_KEY: Your Mailosaur API key
    2. MAILOSAUR_SERVER_ID: Your Mailosaur server ID
    3. MAILOSAUR_SERVER_DOMAIN: Your Mailosaur server domain
    
    You can get these values from your Mailosaur account at https://mailosaur.com/app/servers
    """
    try:
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
    except ValueError as e:
        click.echo(str(e), err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error verifying email: {str(e)}", err=True)
        raise click.Abort() 