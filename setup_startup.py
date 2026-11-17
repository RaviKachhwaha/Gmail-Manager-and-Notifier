import os
import sys

def add_to_startup():
    file_path = os.path.dirname(os.path.abspath(__file__))
    bat_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    bat_file = os.path.join(bat_path, 'GmailAssistant.bat')
    
    # Use pythonw.exe to run without a console window
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    main_script = os.path.join(file_path, "main_service.py")
    
    with open(bat_file, "w+") as bat:
        bat.write(f'@echo off\n')
        bat.write(f'cd /d "{file_path}"\n')
        bat.write(f'start "" "{python_exe}" "{main_script}"\n')
        
    print(f"Added to startup: {bat_file}")
    print("The Gmail AI Assistant will now start automatically when you turn on your PC.")

if __name__ == '__main__':
    add_to_startup()
