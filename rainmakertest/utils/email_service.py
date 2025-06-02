import uuid
import re
import time
from bs4 import BeautifulSoup
import random
import os
try:
    from mailosaur import MailosaurClient
except ImportError:
    raise ImportError(
        "Mailosaur package not found. Please install it with: pip install mailosaur"
    )


class EmailService:
    # Default Mailosaur credentials
    DEFAULT_API_KEY = "GiK6loPqffzz84xt"
    DEFAULT_SERVER_ID = "rhgabfsb"
    DEFAULT_SERVER_DOMAIN = "rhgabfsb.mailosaur.net"

    def __init__(self):
        # Try to get from environment variables first, fall back to defaults
        self.api_key = os.getenv('MAILOSAUR_API_KEY', self.DEFAULT_API_KEY)
        self.server_id = os.getenv('MAILOSAUR_SERVER_ID', self.DEFAULT_SERVER_ID)
        self.server_domain = os.getenv('MAILOSAUR_SERVER_DOMAIN', self.DEFAULT_SERVER_DOMAIN)
        
        if not all([self.api_key, self.server_id, self.server_domain]):
            missing_vars = []
            if not self.api_key:
                missing_vars.append('MAILOSAUR_API_KEY')
            if not self.server_id:
                missing_vars.append('MAILOSAUR_SERVER_ID')
            if not self.server_domain:
                missing_vars.append('MAILOSAUR_SERVER_DOMAIN')
            
            error_msg = (
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please set these environment variables:\n"
                "1. MAILOSAUR_API_KEY: Your Mailosaur API key\n"
                "2. MAILOSAUR_SERVER_ID: Your Mailosaur server ID\n"
                "3. MAILOSAUR_SERVER_DOMAIN: Your Mailosaur server domain\n\n"
                "You can get these values from your Mailosaur account at https://mailosaur.com/app/servers"
            )
            raise ValueError(error_msg)
            
        try:
            self.client = MailosaurClient(self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Mailosaur client: {str(e)}")

    def generate_random_email(self):
        """Generate a random email address using UUID with the mailosaur domain"""
        try:
            # Generate a UUID and remove hyphens
            uuid_str = str(uuid.uuid4()).replace('-', '')
            # Take first 8-12 characters (adjust length as needed)
            username = uuid_str[:random.randint(8, 12)]
            return f"{username}@{self.server_domain}"
        except Exception as e:
            raise RuntimeError(f"Failed to generate random email: {str(e)}")

    def get_verification_code(self, email_address, max_retries=3, delay=5):
        """Retrieve the verification code from an email"""
        for attempt in range(max_retries):
            try:
                email_dict = self._read_email(email_address)
                if not email_dict:
                    time.sleep(delay)
                    continue

                for subject, html in email_dict.items():
                    try:
                        soup = BeautifulSoup(html, 'html.parser')
                        text = soup.get_text()

                        # Improved pattern matching for different email formats
                        patterns = [
                            # Pattern for simple one-line emails
                            r'(?:verification|code)[\s:]*(\d{6})\b',
                            # Pattern for Espressif formatted emails
                            r'Your verification code is (\d{6})',
                            # Generic 6-digit code anywhere in text
                            r'\b\d{6}\b',
                            # Pattern for "Code: 123456" format
                            r'[cC]ode:\s*(\d{6})',
                            # Pattern for "Your code is 123456" format
                            r'[yY]our code is\s*(\d{6})'
                        ]

                        # Try all patterns in order
                        for pattern in patterns:
                            matches = re.findall(pattern, text)
                            if matches:
                                # Return the first 6-digit code found
                                for match in matches:
                                    if len(match) == 6 and match.isdigit():
                                        return match

                    except Exception as e:
                        continue

                time.sleep(delay)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to get verification code after {max_retries} attempts: {str(e)}")
                time.sleep(delay)

        return None

    def _read_email(self, email_address, max_emails=1, max_pages=1):
        """Read emails from the mailbox, optimized for getting the most recent email"""
        try:
            # Get only the most recent messages first
            messages = self.client.messages.list(
                self.server_id,
                page=0,  # First page only
                items_per_page=10,  # Limit to 10 most recent messages
                received_after=None  # Get all messages regardless of age
            )

            if not messages.items:
                return {}

            # Filter messages for the specific email address
            filtered_messages = [
                msg for msg in messages.items
                if email_address in [to.email for to in msg.to]
            ]

            # Sort by received time, most recent first
            filtered_messages.sort(key=lambda x: x.received, reverse=True)
            
            # Take only the most recent email
            filtered_messages = filtered_messages[:max_emails]

            email_dict = {}
            for message_summary in filtered_messages:
                try:
                    full_message = self.client.messages.get_by_id(message_summary.id)
                    if hasattr(full_message, 'html') and full_message.html:
                        email_dict[full_message.subject] = full_message.html.body
                except Exception:
                    continue

            return email_dict
        except Exception as e:
            raise RuntimeError(f"Failed to read emails: {str(e)}")

    def delete_emails(self, email_address):
        """Delete all emails for a given address"""
        try:
            messages = self.client.messages.list(self.server_id)
            filtered_messages = [
                msg for msg in messages.items
                if email_address in [to.email for to in msg.to]
            ]

            for message in filtered_messages:
                self.client.messages.delete(message.id)

            return len(filtered_messages)
        except Exception as e:
            raise RuntimeError(f"Failed to delete emails: {str(e)}")
