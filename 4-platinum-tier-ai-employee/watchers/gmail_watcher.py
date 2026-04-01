"""
Gmail Watcher for AI Employee Silver Tier
Monitors Gmail for new unread/important messages and creates action items
"""
import time
import logging
from pathlib import Path
from datetime import datetime
import sys
import os
import base64

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher


class GmailWatcher(BaseWatcher):
    """Watches Gmail for new messages"""
    
    def __init__(self, project_path: str, check_interval: int = 120):
        self.project_path = Path(project_path)
        self.needs_action = self.project_path / 'needs_action'
        self.check_interval = check_interval
        self.processed_ids = set()
        self.service = None
        self.demo_mode = True  # Default to demo mode
        
        # Setup logging
        log_dir = self.project_path / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'gmail_watcher_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create required directories
        self.needs_action.mkdir(exist_ok=True)
        
        # Try to initialize Gmail service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the Gmail API service"""
        try:
            # Check if credentials exist
            env_file = self.project_path / '.env'
            if env_file.exists():
                from dotenv import load_dotenv
                load_dotenv(env_file)

            client_id = os.getenv('GMAIL_CLIENT_ID')
            client_secret = os.getenv('GMAIL_CLIENT_SECRET')
            refresh_token = os.getenv('GMAIL_REFRESH_TOKEN')
            gmail_token = os.getenv('GMAIL_TOKEN')  # Pre-generated access token

            if not all([client_id, client_secret, refresh_token]):
                self.logger.warning("Gmail credentials not configured. Running in demo mode.")
                self.demo_mode = True
                return

            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from google.auth.transport.requests import Request

            # Try using existing token first, otherwise use refresh token
            if gmail_token:
                self.logger.info("Using existing GMAIL_TOKEN")
                credentials = Credentials(
                    gmail_token,  # Use existing access token
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=client_id,
                    client_secret=client_secret,
                )
            else:
                credentials = Credentials(
                    None,  # No access token initially
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=client_id,
                    client_secret=client_secret,
                )

            # Refresh to get access token
            try:
                credentials.refresh(Request())
                self.service = build('gmail', 'v1', credentials=credentials)
                self.demo_mode = False
                self.logger.info("Gmail service initialized successfully")
                self.logger.info(f"Watching Gmail with credentials for client: {client_id[:20]}...")
            except Exception as refresh_error:
                self.logger.error(f"Token refresh failed: {refresh_error}")
                self.logger.info("Attempting to reinitialize with refresh token...")

                # Try creating new credentials with just refresh token
                credentials = Credentials(
                    None,
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=client_id,
                    client_secret=client_secret,
                )
                credentials.refresh(Request())
                self.service = build('gmail', 'v1', credentials=credentials)
                self.demo_mode = False
                self.logger.info("Gmail service reinitialized successfully")

        except Exception as e:
            self.logger.warning(f"Could not initialize Gmail service: {e}. Running in demo mode.")
            self.logger.warning("To fix: Run generate_gmail_token.py to get new credentials")
            self.demo_mode = True
            self.service = None
    
    def check_for_updates(self) -> list:
        """Check for new unread Gmail messages"""
        if self.demo_mode or self.service is None:
            return self._demo_check()
        
        try:
            # Search for unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]
            
            return new_messages
            
        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []
    
    def _demo_check(self) -> list:
        """Demo mode - simulate checking for emails"""
        # In demo mode, check for demo email files
        demo_file = self.project_path / 'inbox' / 'demo_email.txt'
        if demo_file.exists():
            content = demo_file.read_text()
            demo_file.unlink()  # Remove after processing
            
            return [{
                'id': f'demo_{datetime.now().timestamp()}',
                'from': 'demo@example.com',
                'subject': 'Demo Email',
                'content': content
            }]
        return []
    
    def create_action_file(self, message) -> Path:
        """Create an action file in needs_action folder for the email"""
        try:
            if self.demo_mode or self.service is None:
                return self._create_demo_action_file(message)
            
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            
            # Get body content
            body = self._extract_body(msg)
            
            # Determine priority
            subject = headers.get('Subject', '').lower()
            from_email = headers.get('From', '').lower()
            priority = self._determine_priority(subject, from_email)
            
            content = f"""---
type: email
from: {headers.get('From', 'Unknown')}
to: {headers.get('To', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
message_id: {message['id']}
priority: {priority}
status: pending
labels: {', '.join(msg.get('labelIds', []))}
---

# Email Received

## Header Information
- **From**: {headers.get('From', 'Unknown')}
- **To**: {headers.get('To', 'Unknown')}
- **Subject**: {headers.get('Subject', 'No Subject')}
- **Date**: {headers.get('Date', 'Unknown')}
- **Message ID**: {message['id']}

## Email Content
{body}

## Suggested Actions
- [ ] Read and understand the email
- [ ] Draft a response if needed
- [ ] Take any required actions
- [ ] Mark as processed

## Notes
- Priority: {priority}
"""
            
            # Create safe filename from message ID
            safe_id = message['id'].replace('/', '_')
            filepath = self.needs_action / f'EMAIL_{safe_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            filepath.write_text(content, encoding='utf-8')
            
            self.processed_ids.add(message['id'])
            self.logger.info(f"Action file created for email: {filepath}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error creating action file for email: {e}")
            return None
    
    def _extract_body(self, message) -> str:
        """Extract the body content from a Gmail message"""
        try:
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body_data = part['body'].get('data', '')
                        if body_data:
                            return base64.urlsafe_b64decode(body_data).decode('utf-8')
            
            # Fallback to snippet
            return message.get('snippet', 'No content available')
            
        except Exception as e:
            return f"Error extracting body: {e}"
    
    def _determine_priority(self, subject: str, from_email: str) -> str:
        """Determine email priority based on content"""
        high_priority_keywords = ['urgent', 'asap', 'immediate', 'important', 'invoice', 'payment', 'deadline']
        medium_priority_keywords = ['meeting', 'schedule', 'update', 'review', 'feedback']
        
        for keyword in high_priority_keywords:
            if keyword in subject:
                return 'high'
        
        for keyword in medium_priority_keywords:
            if keyword in subject:
                return 'medium'
        
        return 'normal'
    
    def _create_demo_action_file(self, message_data: dict) -> Path:
        """Create a demo action file when running without credentials"""
        content = f"""---
type: email
from: {message_data.get('from', 'demo@example.com')}
subject: {message_data.get('subject', 'Demo Email')}
received: {datetime.now().isoformat()}
priority: normal
status: pending
demo_mode: true
---

# Demo Email (Gmail Watcher in Demo Mode)

## Note
The Gmail Watcher is running in demo mode because credentials are not configured.

## To Enable Real Gmail Monitoring:
1. Set up a Google Cloud Project
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Add credentials to .env file

## Demo Email Content
- **From**: {message_data.get('from', 'demo@example.com')}
- **Subject**: {message_data.get('subject', 'Demo Email')}
- **Content**: {message_data.get('content', 'No content')}

## Suggested Actions
- [ ] Configure Gmail API credentials
- [ ] Re-run the watcher with proper authentication
"""
        
        filepath = self.needs_action / f'EMAIL_DEMO_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        filepath.write_text(content, encoding='utf-8')
        return filepath
    
    def run(self):
        """Start watching Gmail"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')
        self.logger.info(f'Demo mode: {self.demo_mode}')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    for item in items:
                        self.create_action_file(item)
                    
                    if items:
                        self.logger.info(f"Processed {len(items)} new emails")
                        
                except Exception as e:
                    self.logger.error(f"Error during check: {e}")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Gmail watcher stopped by user")
        except Exception as e:
            self.logger.error(f"Error in Gmail watcher: {e}")
            raise


def run_example():
    """Example of how to use the Gmail Watcher"""
    watcher = GmailWatcher(str(project_root), check_interval=30)
    print(f"Gmail Watcher initialized. Demo mode: {watcher.demo_mode}")
    print("Starting to watch for new emails...")
    watcher.run()


if __name__ == "__main__":
    run_example()
