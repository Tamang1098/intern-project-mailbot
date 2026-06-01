import smtplib

def send_email(email, password, msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)

        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("SMTP Error:", e)
        return False