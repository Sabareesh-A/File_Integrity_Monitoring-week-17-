import os
import hashlib
import time
import json
import smtplib
from email.mime.text import MIMEText

folder_path = "/Users/sabareeshanil/Desktop/fim/alert fim email/file-dir"

LOG_FILE = "fim_log.log"


# ---------- Email Alert ----------
def send_email_alert(file_name, old_hash, new_hash, severity, timestamp):

    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")

    body = f"""
FIM Alert ⚠️

File: {file_name}
Severity: {severity}

Old Hash: {old_hash}
New Hash: {new_hash}

Time: {timestamp}
"""

    msg = MIMEText(body)
    msg["Subject"] = "File Integrity Monitoring Alert"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


# ---------- Log Writer ----------
def write_log(file_name, old_hash, new_hash, severity, timestamp):

    log_entry = f"""
{timestamp}
File: {file_name}
Severity: {severity}
Old Hash: {old_hash}
New Hash: {new_hash}
----------------------------------
"""

    with open(LOG_FILE, "a") as log:
        log.write(log_entry)


# ------- File hash calculation -----
def process_file(file_path, new_hashes):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    file_name = os.path.basename(file_path)
    current_time = time.ctime()

    new_hashes[file_name] = {
        "hash": file_hash,
        "timestamp": current_time
    }


# --------- Severity check -------
def get_priority(file_name):
    if 'passwd' in file_name or 'shadow' in file_name:
        return "critical"
    elif file_name.endswith(".exe") or file_name.endswith(".sh"):
        return "high"
    elif file_name.endswith(".log"):
        return "medium"
    else:
        return "low"


# -------- Create baseline --------
if not os.path.exists("baseline.json"):
    initial_hashes = {}
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            process_file(full_path, initial_hashes)

    with open("baseline.json", "w") as f:
        json.dump(initial_hashes, f, indent=4)


# -------- Monitoring Loop --------
while True:

    new_hashes = {}

    priority = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path):
            process_file(full_path, new_hashes)

    with open("baseline.json", "r") as f:
        existing_hashes = json.load(f)

    # -------- Modified Files --------
    for file in existing_hashes:

        if file in new_hashes:

            if existing_hashes[file]["hash"] != new_hashes[file]["hash"]:

                severity = get_priority(file)

                old_hash = existing_hashes[file]["hash"]
                new_hash = new_hashes[file]["hash"]
                timestamp = new_hashes[file]["timestamp"]

                priority[severity].append(file + " modified at " + timestamp)

                write_log(file, old_hash, new_hash, severity, timestamp)

                if severity in ["critical", "high"]:
                    send_email_alert(file, old_hash, new_hash, severity, timestamp)

    # -------- Deleted Files --------
    for file in existing_hashes:

        if file not in new_hashes:

            severity = get_priority(file)
            timestamp = time.ctime()

            priority[severity].append(file + " deleted at " + timestamp)

            write_log(file, existing_hashes[file]["hash"], "DELETED", severity, timestamp)

    # -------- Added Files --------
    for file in new_hashes:

        if file not in existing_hashes:

            severity = get_priority(file)
            timestamp = new_hashes[file]["timestamp"]

            priority[severity].append(file + " added at " + timestamp)

            write_log(file, "NEW FILE", new_hashes[file]["hash"], severity, timestamp)

    with open("priority.json", "w") as f:
        json.dump(priority, f, indent=4)

    with open("baseline.json", "w") as f:
        json.dump(new_hashes, f, indent=4)

    if priority["critical"] or priority["high"]:
        print("⚠️ Critical or High Priority Changes Detected")

    time.sleep(10)