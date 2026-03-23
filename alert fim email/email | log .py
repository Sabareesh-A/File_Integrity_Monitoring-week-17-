import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

LOG_FILE = "fim_log.log"

def send_email_alert(file_name, old_hash, new_hash, severity):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---- Create Log Entry ----
    log_entry = f"""
Timestamp : {timestamp}
File      : {file_name}
Severity  : {severity}
Old Hash  : {old_hash}
New Hash  : {new_hash}
-------------------------------------
"""

    with open(LOG_FILE, "a") as log:
        log.write(log_entry)

    # ---- Email Content ----
    sender = "sabareeshanil02@gmail.com"
    receiver = "sabareesha.dev@gmail.com"
    password = "YOUR_APP_PASSWORD"

    subject = "⚠️ FIM Alert - File Modified"

    body = f"""
File Integrity Monitoring Alert

Timestamp : {timestamp}
File Name : {file_name}
Severity  : {severity}

Old Hash  : {old_hash}
New Hash  : {new_hash}

Check the attached log file for history.
"""

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # ---- Attach Log File ----
    with open(LOG_FILE, "rb") as f:
        attach = MIMEApplication(f.read(), Name=LOG_FILE)
        attach['Content-Disposition'] = f'attachment; filename="{LOG_FILE}"'
        msg.attach(attach)

    # ---- Send Email ----
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()