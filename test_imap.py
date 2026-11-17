import sys
from imap_tools import MailBox, AND

GMAIL_USER = "your_email@gmail.com"
GMAIL_PASS = "xxxx xxxx xxxx xxxx"
IMAP_SERVER = "imap.gmail.com"

try:
    with MailBox(IMAP_SERVER).login(GMAIL_USER, GMAIL_PASS) as mailbox:
        print("Checking with X-GM-RAW...")
        emails = mailbox.fetch('UNSEEN X-GM-RAW "category:primary"', limit=5)
        for msg in emails:
            print(f"UID: {msg.uid}, Subject: {msg.subject}")
            
        print("Checking with A(...) ...")
        # try A() or just iterate to see labels
        emails2 = mailbox.fetch(AND(seen=False), limit=5)
        for msg in emails2:
            print(f"Subject: {msg.subject}")
            if hasattr(msg, 'labels'):
                print(f"Labels: {msg.labels}")
            
except Exception as e:
    print(f"Error: {e}")
