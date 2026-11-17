import os
from winotify import Notification, audio

def Alert(Text, title, url_show="", url_detail=""):
    # Resolve animation icon path relative to this file, with fallback
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_icon = os.path.join(base_dir, "animation_For_Alert2.gif")
    icon_path = local_icon if os.path.exists(local_icon) else r"C:\Users\Admin\Desktop\JARVIS\animation_For_Alert2.gif"

    toast = Notification(
        app_id="J A R V I S ®",
        title=title, # title="🟢  Alert  🟢",
        msg=Text,  # Use the Text argument here
        duration="short",
        icon=icon_path
        #launch: str = '' also Available this can do launch: The url or callback to launch (invoked when the user clicks the notification)
    )

    toast.set_audio(audio.Default, loop=False)

    if url_show:
        toast.add_actions(label="Summarize (Voice)", launch=url_show) 
    if url_detail:
        toast.add_actions(label="Details (Voice)", launch=url_detail)

    toast.show()

# Alert("Test Done For GIF And As Now No Changes Mey Required.", "Hello Sir")