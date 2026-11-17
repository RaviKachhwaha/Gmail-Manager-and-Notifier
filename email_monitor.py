import re
import html
from imap_tools import MailBox, AND

GMAIL_USER = "your_email@gmail.com"
GMAIL_PASS = "xxxx xxxx xxxx xxxx"
IMAP_SERVER = "imap.gmail.com"

def _strip_html(raw_html):
    """Remove HTML tags and decode entities to get plain text."""
    if not raw_html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_unread_emails():
    """Fetch all unread emails from Gmail and return them as a list of dicts."""
    try:
        with MailBox(IMAP_SERVER).login(GMAIL_USER, GMAIL_PASS) as mailbox:
            emails = []
            for msg in mailbox.fetch('UNSEEN X-GM-RAW "category:primary"', limit=50, reverse=True, mark_seen=False):
                # Prefer plain text body; fall back to stripped HTML
                body = msg.text if msg.text else _strip_html(msg.html)
                emails.append({
                    "uid": msg.uid,
                    "sender": msg.from_,
                    "subject": msg.subject or "(No Subject)",
                    "body": body or "(Empty body)",
                    "date": str(msg.date),
                })
            return emails
    except Exception as e:
        print(f"[EmailMonitor] Error fetching emails: {e}")
        return []

def mark_as_seen(uid):
    """Mark a single email as seen/read by its UID."""
    try:
        with MailBox(IMAP_SERVER).login(GMAIL_USER, GMAIL_PASS) as mailbox:
            mailbox.seen(mailbox.fetch(AND(uid=uid)), True)
    except Exception as e:
        print(f"[EmailMonitor] Error marking email {uid} as seen: {e}")

if __name__ == "__main__":
    emails = get_unread_emails()
    for e in emails:
        print(f"From: {e['sender']} | Subject: {e['subject']}")
    print(f"Total unread: {len(emails)}")
