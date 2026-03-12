"""
Email Tool
Send, read, reply to emails.
"""

import logging
from typing import Dict, Any, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import config

logger = logging.getLogger(__name__)


class EmailTool:
    """Email operations."""
    
    def __init__(self):
        """Initialize email tool."""
        self.smtp_server = config.email.smtp_server
        self.smtp_port = config.email.smtp_port
        self.email = config.email.smtp_email
        self.password = config.email.smtp_password
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Send email.
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            html: HTML email flag
            attachments: File paths to attach
            
        Returns:
            dict: {success, result, error}
        """
        try:
            msg = MIMEMultipart("alternative" if html else "mixed")
            msg["From"] = self.email
            msg["To"] = to
            msg["Subject"] = subject
            
            content_type = "html" if html else "plain"
            msg.attach(MIMEText(body, content_type))
            
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, "rb") as attachment:
                            part = MIMEText(attachment.read())
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {file_path}",
                            )
                            msg.attach(part)
                    except Exception as e:
                        logger.warning(f"Failed to attach {file_path}: {str(e)}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to}")
            return {
                "success": True,
                "result": f"Sent to {to}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Send email failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def read_inbox(self, limit: int = 10) -> Dict[str, Any]:
        """
        Read inbox emails.
        
        Args:
            limit: Max emails to retrieve
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import imaplib
            
            imap = imaplib.IMAP4_SSL(self.smtp_server)
            imap.login(self.email, self.password)
            imap.select("INBOX")
            
            _, data = imap.search(None, "ALL")
            email_ids = data[0].split()[-limit:]
            
            emails = []
            for email_id in email_ids:
                _, msg_data = imap.fetch(email_id, "(RFC822)")
                emails.append({"id": email_id.decode(), "data": msg_data})
            
            imap.close()
            
            logger.info(f"Read {len(emails)} emails")
            return {
                "success": True,
                "result": emails,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Read inbox failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    def reply_email(
        self,
        to: str,
        subject: str,
        body: str,
        in_reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Reply to email.
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            in_reply_to: Original message ID
            
        Returns:
            dict: {success, result, error}
        """
        try:
            msg = MIMEText(body)
            msg["From"] = self.email
            msg["To"] = to
            msg["Subject"] = f"Re: {subject}"
            
            if in_reply_to:
                msg["In-Reply-To"] = in_reply_to
                msg["References"] = in_reply_to
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            logger.info(f"Reply sent to {to}")
            return {
                "success": True,
                "result": f"Reply sent to {to}",
                "error": None,
            }
        except Exception as e:
            logger.error(f"Reply email failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }
    
    async def search_emails(self, query: str) -> Dict[str, Any]:
        """
        Search emails.
        
        Args:
            query: Search query
            
        Returns:
            dict: {success, result, error}
        """
        try:
            import imaplib
            
            imap = imaplib.IMAP4_SSL(self.smtp_server)
            imap.login(self.email, self.password)
            imap.select("INBOX")
            
            _, data = imap.search(None, "ALL", query)
            email_ids = data[0].split()
            
            imap.close()
            
            logger.info(f"Found {len(email_ids)} emails matching '{query}'")
            return {
                "success": True,
                "result": [eid.decode() for eid in email_ids],
                "error": None,
            }
        except Exception as e:
            logger.error(f"Search emails failed: {str(e)}")
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }


# Global instance
email_tool = EmailTool()


def send_email(
    to: str,
    subject: str,
    body: str,
    html: bool = False,
) -> Dict[str, Any]:
    """Send email wrapper."""
    return email_tool.send_email(to, subject, body, html)
