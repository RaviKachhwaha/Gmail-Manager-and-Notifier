# Gmail Manager and Notifier

A lightweight Windows background tool that watches your primary Gmail inbox, pops up native desktop notifications, and reads out quick AI summaries or full details when you click a button.

## Features

- **Background Inbox Monitoring**: Checks your primary Gmail inbox every 30 seconds via IMAP without needing a browser open.
- **Native Windows Notifications**: Shows interactive Windows 10/11 toast alerts with action buttons.
- **Voice Summaries**: Uses GPT-4o (`g4f`) and Microsoft Edge TTS to read aloud either a quick 2–3 sentence summary or a detailed breakdown of deadlines and tasks.
- **Smart Reminders**:
  - **0 min**: Initial desktop alert.
  - **10 min**: Second visual reminder if still unread.
  - **20 min**: Final alert plus a spoken voice reminder.
- **Auto-Start Support**: Includes scripts to add or remove the assistant from Windows Startup.
- **CSV Mail Sender**: Comes with `Gmail.py` to quickly send emails to contacts saved in a CSV file.

## Requirements:-
Windows 10 or 11

Python 3.10 – 3.12 (make sure "Add Python to PATH" is checked during install)

A Gmail account with 2-Step Verification and IMAP enabled

Setup
1. Get a Gmail App Password
Go to Google Account Security and make sure 2-Step Verification is ON.

Search for App passwords, create one named Gmail Assistant, and copy the 16-character password.

In Gmail web settings, go to See all settings > Forwarding and POP/IMAP, select Enable IMAP, and save changes.

2. Install Dependencies
```Bash
git clone [https://github.com/RaviKachhwaha/Gmail-Manager-and-Notifier](https://github.com/RaviKachhwaha/Gmail-Manager-and-Notifier)
cd Gmail-Manager-and-Notifier
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Add Your Credentials
Open email_monitor.py, Gmail.py, and test_imap.py, and add your email and App Password:

```Python
GMAIL_USER = "your_email@gmail.com"
GMAIL_PASS = "xxxx xxxx xxxx xxxx"
```
(Optional) Copy contacts.csv.example to contacts.csv if you want to use the CSV email sender:

```PowerShell
Copy-Item contacts.csv.example contacts.csv
```

## Usage

Test notifications and voice:

```Bash
python test_system.py
```

Run in the foreground (with console logs):

```Bash
python main_service.py
```

Run silently in the background:

```Bash
pythonw main_service.py
```

(Logs are saved to gmail_assistant.log.)

Manage Windows Startup:

Enable: python setup_startup.py

Disable: python disable_startup.py

Send an email via CSV:

```Bash
python Gmail.py
```

Customization
Change the voice: Edit VOICE in voice_tts.py (default is en-IN-PrabhatNeural; other options include en-US-ChristopherNeural, en-GB-RyanNeural, or en-US-AriaNeural).

Adjust check intervals: Change CHECK_INTERVAL_SECONDS (default 30) and REMINDER_INTERVAL_SECONDS (default 600) in main_service.py.

Change alert icon: Replace animation_For_Alert2.gif with your own .gif or .png.

Troubleshooting
Authentication failed: Make sure you are using your 16-character App Password, not your regular Gmail password.

No notifications showing: Check that Windows Focus Assist / Do Not Disturb is turned off.

Port 50555 already in use: Close any existing pythonw.exe process in Task Manager or change HTTP_PORT in main_service.py.

No audio: Verify your Windows default playback device is connected and unmuted.

License
MIT License. See LICENSE for details.
