"""
Gmail AI Assistant — Main Background Service
Runs silently, monitors Gmail for new mail, shows system alerts via Alert.py,
uses g4f for AI summarization/details, and Edge TTS for voice output.
"""

import sys
import os
import time
import threading
import logging
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Setup logging to a file (since .pyw has no console)
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gmail_assistant.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("GmailAssistant")

import email_monitor
import ai_processor
import voice_tts
from Alert import Alert

# ── Configuration ──────────────────────────────────────────────
CHECK_INTERVAL_SECONDS = 30       # How often to poll Gmail
REMINDER_INTERVAL_SECONDS = 600   # 10 minutes between alerts
HTTP_PORT = 50555                 # Port for background action server
# ───────────────────────────────────────────────────────────────

# Global dictionary to store email state
# { uid: {'mail': dict, 'alert_count': int, 'last_alert_time': float} }
email_state = {}


def process_show(uid):
    """Summarize the email with AI, then speak the summary aloud."""
    state = email_state.get(uid)
    if not state:
        log.warning(f"Email UID {uid} not found in state for summarization.")
        return
    state['alert_count'] = 3 # Stop future reminders since user interacted
    email = state['mail']
    body = (email["body"] or "")[:3000]
    log.info(f"Summarizing uid={uid}...")
    summary = ai_processor.summarize_email(email["sender"], email["subject"], body)
    log.info(f"Summary for uid={uid}: {summary[:100]}...")
    voice_tts.speak(str(summary))


def process_details(uid):
    """Get detailed analysis of the email with AI, then speak it aloud."""
    state = email_state.get(uid)
    if not state:
        log.warning(f"Email UID {uid} not found in state for details.")
        return
    state['alert_count'] = 3 # Stop future reminders since user interacted
    email = state['mail']
    body = (email["body"] or "")[:3000]
    log.info(f"Detailing uid={uid}...")
    details = ai_processor.detail_email(email["sender"], email["subject"], body)
    log.info(f"Details for uid={uid}: {details[:100]}...")
    voice_tts.speak(str(details))


def trigger_tts_reminder():
    """Generates and speaks a general reminder that a new email is waiting."""
    log.info("Triggering AI TTS reminder...")
    reminder_text = ai_processor.generate_reminder()
    log.info(f"Reminder TTS text: {reminder_text}")
    voice_tts.speak(str(reminder_text))


class ActionHandler(BaseHTTPRequestHandler):
    """Handles clicks from the system notification buttons."""
    
    def log_message(self, format, *args):
        # Silence default http server logging to avoid spam
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        uid = qs.get("uid", [None])[0]

        # Respond with Javascript to close the browser tab instantly
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Action</title></head><body><script>window.close();</script></body></html>")

        if uid:
            if parsed.path == "/show":
                log.info(f"Action: User requested SHOW (summarize) for UID {uid}")
                threading.Thread(target=process_show, args=(uid,), daemon=True).start()
            elif parsed.path == "/detail":
                log.info(f"Action: User requested DETAIL for UID {uid}")
                threading.Thread(target=process_details, args=(uid,), daemon=True).start()


def run_http_server():
    """Runs the background action server."""
    server_address = ('127.0.0.1', HTTP_PORT)
    try:
        httpd = HTTPServer(server_address, ActionHandler)
        log.info(f"Background HTTP server listening on {HTTP_PORT}...")
        httpd.serve_forever()
    except Exception as e:
        log.error(f"HTTP Server error: {e}")


def check_emails_job():
    """Background thread: polls Gmail for unread emails and manages reminder alerts."""
    log.info("Email monitoring thread started.")
    
    # Track emails that have been permanently dismissed (so they don't pop up again if still unread)
    processed_uids = set()
    
    while True:
        try:
            unread = email_monitor.get_unread_emails()
            current_uids = {mail["uid"]: mail for mail in unread}
            
            # Clean up state for emails that have been read (no longer in unread list)
            for uid in list(email_state.keys()):
                if uid not in current_uids:
                    log.info(f"Email UID {uid} was marked read or removed. Stopping reminders.")
                    del email_state[uid]
                    
            # Process current unread emails
            for uid, mail in current_uids.items():
                # If we haven't seen this email before, add to state and send Alert 1
                if uid not in email_state:
                    log.info(f"New mail: uid={uid} from={mail['sender']} subj={mail['subject']}")
                    email_state[uid] = {
                        'mail': mail,
                        'alert_count': 1,
                        'last_alert_time': time.time()
                    }
                    trigger_alert(uid, mail, attempt=1)
                else:
                    # Check if it's time for a reminder
                    state = email_state[uid]
                    time_since_last = time.time() - state['last_alert_time']
                    
                    if time_since_last >= REMINDER_INTERVAL_SECONDS:
                        if state['alert_count'] == 1:
                            # 10 minutes passed -> Alert 2
                            log.info(f"10-min reminder for UID {uid}")
                            state['alert_count'] = 2
                            state['last_alert_time'] = time.time()
                            trigger_alert(uid, mail, attempt=2)
                            
                        elif state['alert_count'] == 2:
                            # 20 minutes passed -> Alert 3 + TTS
                            log.info(f"20-min final reminder for UID {uid}")
                            state['alert_count'] = 3
                            state['last_alert_time'] = time.time()
                            trigger_alert(uid, mail, attempt=3)
                            
                            # Run TTS reminder in a thread so we don't block the loop
                            threading.Thread(target=trigger_tts_reminder, daemon=True).start()
                            
        except Exception as e:
            log.error(f"Email check error: {e}")
            try:
                Alert(f"Email check error: {str(e)}", "⚠️ System Error")
            except Exception as alert_e:
                log.error(f"Failed to send error alert: {alert_e}")
            
        try:
            time.sleep(CHECK_INTERVAL_SECONDS)
        except Exception:
            pass


def trigger_alert(uid, mail, attempt):
    """Helper to display the system notification."""
    title = f"📩  {'Reminder: ' if attempt > 1 else ''}New Mail"
    message = f"From: {mail['sender']}\nSubject: {mail['subject']}"
    url_show = f"http://127.0.0.1:{HTTP_PORT}/show?uid={uid}"
    url_detail = f"http://127.0.0.1:{HTTP_PORT}/detail?uid={uid}"
    
    # Display using the custom Alert.py system
    Alert(message, title, url_show=url_show, url_detail=url_detail)


if __name__ == "__main__":
    log.info("=" * 50)
    log.info("Gmail AI Assistant (Jarvis Mode) starting up.")
    log.info("=" * 50)

    # Start the HTTP server for action buttons
    threading.Thread(target=run_http_server, daemon=True).start()

    # The email check loop runs in the main thread (blocking)
    while True:
        try:
            check_emails_job()
        except Exception as e:
            log.error(f"Fatal error in check_emails_job: {e}")
            try:
                Alert(f"Fatal error: {str(e)}", "🛑 Service Restarting")
            except:
                pass
            time.sleep(10)
