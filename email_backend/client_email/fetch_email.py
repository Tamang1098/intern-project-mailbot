import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def fetch_latest_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, EMAIL_PASSWORD)

    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")
    email_ids = data[0].split()

    if not email_ids:
        return None, None, None, None

    latest_id = email_ids[-1]
    result, msg_data = mail.fetch(latest_id, "(RFC822)")

    msg = email.message_from_bytes(msg_data[0][1])

    subject = msg["subject"]
    sender = msg["from"]

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    mail.store(latest_id, "+FLAGS", "\\Seen")
    mail.logout()

    return subject, sender, body, latest_id