import smtplib
from email.message import EmailMessage
from typing import Dict, Any
from config import settings

class EmailTool:
    """Sends emails via SMTP."""
    
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASS

    async def run(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Sends an email message."""
        if not all([self.host, self.user, self.password]):
            return {"error": "Email configuration missing"}

        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = self.user
            msg['To'] = to

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
                
            return {"status": "sent", "to": to}
            
        except Exception as e:
            return {"error": str(e)}
