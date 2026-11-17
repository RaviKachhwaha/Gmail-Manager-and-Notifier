import time
import threading
import main_service

def run_test():
    print("Starting background HTTP server for action buttons...")
    threading.Thread(target=main_service.run_http_server, daemon=True).start()
    
    # Simulate a fake email entering the system
    fake_uid = "9999"
    fake_email = {
        "uid": fake_uid,
        "sender": "boss@company.com",
        "subject": "Urgent: Project Update",
        "body": "Hello, please review the latest designs for the project. We need to deploy them by tomorrow morning. Do not ignore this message. Best, Boss.",
        "date": "Today"
    }
    
    print("Mocking email into state...")
    main_service.email_state[fake_uid] = {
        'mail': fake_email,
        'alert_count': 1,
        'last_alert_time': time.time()
    }
    
    print("Triggering system alert...")
    title = "📩  New Mail (TEST)"
    message = f"From: {fake_email['sender']}\nSubject: {fake_email['subject']}"
    url_show = f"http://127.0.0.1:{main_service.HTTP_PORT}/show?uid={fake_uid}"
    url_detail = f"http://127.0.0.1:{main_service.HTTP_PORT}/detail?uid={fake_uid}"
    
    main_service.Alert(message, title, url_show=url_show, url_detail=url_detail)
    
    print("Alert triggered! Please click 'Summarize (Voice)' or 'Details (Voice)' on the Windows notification.")
    print("The script will stay alive for 60 seconds to allow you to test the voice features.")
    
    # Keep the script alive so the background thread can process the click and voice output
    time.sleep(60)
    print("Test completed.")

if __name__ == "__main__":
    run_test()
