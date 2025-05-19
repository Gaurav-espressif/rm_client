# utils/email_service.py
import uuid
import re
import time
from bs4 import BeautifulSoup
import random
try:
    from mailosaur import MailosaurClient
except ImportError:
    raise ImportError(
        "Mailosaur package not found. Please install it with: pip install mailosaur"
    )


class EmailService:
    def __init__(self):
        self.api_key = "GiK6loPqffzz84xt"
        self.server_id = "rhgabfsb"
        self.server_domain = "rhgabfsb.mailosaur.net"
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

                        # Look for verification code patterns
                        patterns = [
                            r'(?:Verification|Your Verification) Code is:\s*(\d{6})',
                            r'\b\d{6}\b',
                            r'code:\s*(\d{6})',
                            r'code is\s*(\d{6})'
                        ]

                        for pattern in patterns:
                            match = re.search(pattern, text)
                            if match:
                                return match.group(1)
                    except Exception:
                        continue

                time.sleep(delay)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to get verification code after {max_retries} attempts: {str(e)}")
                time.sleep(delay)

        return None

    def _read_email(self, email_address, max_emails=5, max_pages=5):
        """Read emails from the mailbox"""
        try:
            all_messages = []
            items_per_page = 50

            for page in range(max_pages):
                messages = self.client.messages.list(self.server_id, page=page, items_per_page=items_per_page)
                if not messages.items:
                    break

                all_messages.extend(messages.items)

                if len(messages.items) < items_per_page:
                    break

            filtered_messages = [
                msg for msg in all_messages
                if email_address in [to.email for to in msg.to]
            ]

            filtered_messages.sort(key=lambda x: x.received, reverse=True)
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