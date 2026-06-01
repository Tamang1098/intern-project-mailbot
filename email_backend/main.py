import os
import time
from dotenv import load_dotenv
from email.message import EmailMessage

from client_email.fetch_email import fetch_latest_email
from client_email.send_email import send_email
from category.category import get_category
from config.config import get_receivers
from services.email_repository import save_email

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 3))

processed_emails = set()


def run_bot():
    while True:
        try:
            subject, sender, body, email_id = fetch_latest_email()

            if not subject:
                time.sleep(CHECK_INTERVAL)
                continue

            if email_id in processed_emails:
                time.sleep(CHECK_INTERVAL)
                continue

            processed_emails.add(email_id)

            print("\n📩 NEW EMAIL")
            print("Subject:", subject)
            print("From:", sender)

            category = get_category(subject, body)
            print("📂 Category:", category)

            if not category:
                continue

            receivers = get_receivers(category)
            print("DEBUG receivers:", receivers)

            if not receivers:
                print("⚠ No receivers found")
                continue

            # SAVE TO DB (ONLY ONCE)
            forwarded_list = ", ".join(receivers)
            save_email(sender, subject, body, category, forwarded_list)

            msg = EmailMessage()
            msg["Subject"] = f"FWD: {subject}"
            msg["From"] = EMAIL
            msg["To"] = ", ".join(receivers)

            msg.set_content(f"""
FORWARDED EMAIL

From: {sender}
Subject: {subject}

-------------------
{body}
-------------------
""")

            success = send_email(EMAIL, PASSWORD, msg)

            if success:
                print("📤 Sent to:", receivers)
            else:
                print("❌ Failed to send")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_bot()