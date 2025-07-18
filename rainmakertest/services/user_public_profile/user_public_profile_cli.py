import click
from typing import Optional, List, Dict
import json
import logging
from ...user_public_profile.user_public_profile import UserPublicProfileService
from ...utils.api_client import ApiClient

logger = logging.getLogger(__name__)

@click.group()
def profile():
    """User public profile operations"""
    pass

def parse_profile_data(profile_str: str) -> Dict:
    """Parse profile data string into dictionary
    Format: key1=value1,key2=value2
    Example: name=John,age=30,active=true
    """
    if not profile_str:
        return {}
    
    profile = {}
    try:
        for item in profile_str.split(','):
            if '=' not in item:
                raise ValueError(f"Invalid profile data format: {item}. Expected format: key=value")
            key, value = item.split('=', 1)  # Split only on first '=' to handle values with '='
            
            # Convert value to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.lower() == 'null':
                value = None
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # Keep as string
            
            profile[key.strip()] = value
        
        return profile
    except Exception as e:
        logger.error(f"Error parsing profile data: {str(e)}")
        raise click.UsageError(
            f"Error parsing profile data: {str(e)}\n"
            f"Example format: name=John,age=30,active=true\n"
            f"Make sure to quote the entire profile string if it contains special characters."
        )

@profile.command()
@click.option('--user-name', help='User name to fetch profile for (optional - fetches current user if not provided)')
@click.pass_context
def get(ctx, user_name: Optional[str]):
    """Fetch a user's public profile"""
    try:
        api_client = ctx.obj['api_client']
        profile_service = UserPublicProfileService(api_client)
        
        result = profile_service.get_public_profile(user_name=user_name)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error getting public profile: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@profile.command()
@click.option('--profile-data', 
              help='Profile data in format key1=value1,key2=value2. Use "null" for null values.')
@click.option('--profile-file', type=click.Path(exists=True),
              help='Path to JSON file containing profile data')
@click.option('--delete-profile', is_flag=True,
              help='Delete the entire profile (reset to empty)')
@click.pass_context
def update(ctx, profile_data: Optional[str], profile_file: Optional[str], delete_profile: bool):
    """Add a new or update an existing public profile"""
    try:
        api_client = ctx.obj['api_client']
        profile_service = UserPublicProfileService(api_client)
        
        if delete_profile:
            # Delete entire profile
            profile_dict = None
        elif profile_file:
            # Load profile from JSON file
            with open(profile_file, 'r') as f:
                profile_dict = json.load(f)
        elif profile_data:
            # Parse profile from command line string
            profile_dict = parse_profile_data(profile_data)
        else:
            raise click.UsageError("Either --profile-data, --profile-file, or --delete-profile must be provided")
        
        result = profile_service.update_public_profile(profile=profile_dict)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Error updating public profile: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
