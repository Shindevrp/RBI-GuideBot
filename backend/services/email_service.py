import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, NamedTuple
from backend.core.config import settings

class Email(NamedTuple):
    uid: "YOUR_EMAIL_UID" # Unique identifier for the email`
    from_address: "YOUR_EMAIL_FROM_ADDRESS" # Sender's email address
    subject: "YOUR_EMAIL_SUBJECT" # Subject of the email
    body: "YOUR_EMAIL_BODY" # Body of the email, can be plain text or HTML
    # Add more fields as needed, e.g., date, attachments, etc.
   
    body: "YOUR_EMAIL_BODY" # Body of the email, can be plain text or HTML

def fetch_unread_emails() -> List[Email]:
    """Fetches unread emails from the configured IMAP server."""
    try:
        imap = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
        imap.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
        imap.select("inbox")

        # Search for unread emails
        status, messages = imap.search(None, "UNSEEN")
        if status != "OK":
            return []

        email_list = []
        for num in messages[0].split():
            status, data = imap.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            msg = email.message_from_bytes(data[0][1])
            
            # Decode subject and sender
            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
            from_address = msg.get("From")

            # Get email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            email_list.append(Email(uid=num.decode(), from_address=from_address, subject=subject, body=body))
        
        imap.logout()
        return email_list
    except Exception as e:
        print(f"Failed to fetch emails: {e}")
        return []

def send_reply(to_address: str, subject: str, body: str):
    """Sends a reply email via the configured SMTP server."""
    message = MIMEMultipart()
    message["From"] = settings.SMTP_USER
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_address, message.as_string())
            print(f"Successfully sent email to {to_address}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def mark_as_read(uid: str):
    """Marks an email as read (seen) on the IMAP server."""
    try:
        imap = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
        imap.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
        imap.select("inbox")
        imap.store(uid, '+FLAGS', '\\Seen')
        imap.logout()
    except Exception as e:
        print(f"Failed to mark email {uid} as read: {e}")