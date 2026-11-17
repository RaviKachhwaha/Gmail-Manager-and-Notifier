import smtplib
import csv

# Gmail credentials
GMAIL_USER = "your_email@gmail.com"
GMAIL_PASS = "xxxx xxxx xxxx xxxx"  # Use an App Password, not your main password

# Load email contacts from a CSV file
def load_contacts(filename):
    contacts = {}
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        if 'Name' not in headers or 'Email' not in headers:
            raise KeyError("CSV file must contain 'Name' and 'Email' headers")
        for row in reader:
            contacts[row['Name'].strip()] = row['Email'].strip()
    return contacts

# Send email
def send_email(recipient_email, subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASS)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(GMAIL_USER, recipient_email, email_message)
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main workflow
def main():
    contacts = load_contacts("contacts.csv")
    recipient_name = input("Enter recipient name: ").strip()
    
    if recipient_name in contacts:
        subject = input("Enter email subject: ").strip()
        message = input("Enter your message: ").strip()
        recipient_email = contacts[recipient_name]
        send_email(recipient_email, subject, message)
    else:
        print(f"No contact found for {recipient_name}")

main()
