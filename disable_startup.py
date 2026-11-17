import os

def disable_startup():
    bat_file = os.path.join(
        os.getenv('APPDATA'),
        r'Microsoft\Windows\Start Menu\Programs\Startup',
        'GmailAssistant.bat'
    )
    if os.path.exists(bat_file):
        os.remove(bat_file)
        print("✅ Gmail AI Assistant auto-start has been DISABLED.")
        print(f"   Removed: {bat_file}")
    else:
        print("ℹ️  Auto-start was already disabled (batch file not found).")

if __name__ == '__main__':
    disable_startup()
