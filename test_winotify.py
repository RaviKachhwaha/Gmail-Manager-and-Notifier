import os
from winotify import Notification, audio

def test_alert():
    toast = Notification(
        app_id="J A R V I S ®",
        title="Test Alert",
        msg="Testing winotify launch",
        duration="short"
    )
    # create a dummy bat file
    bat_path = os.path.abspath("test_launch.bat")
    with open(bat_path, "w") as f:
        f.write("echo 'Hello from winotify' > test_launch_output.txt")
    
    toast.add_actions(label="Run Bat", launch=bat_path)
    toast.show()

if __name__ == "__main__":
    test_alert()
