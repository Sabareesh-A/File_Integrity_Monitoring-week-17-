import os
import hashlib
import time
import json
import smtplib
from email.mime.text import MIMEText
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

folder_path = "/Users/sabareeshanil/Desktop/fim/project/file-dir"

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

    try:
        msg = MIMEText(body)
        msg["Subject"] = "File Integrity Monitoring Alert"
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        print("Email alert sent")

    except Exception as e:
        print("Email sending failed:", e)


# ---------- Jira Setup ----------
JIRA_URL = os.getenv("JIRA_URL")
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")


# ---------- Jira Ticket ----------
def create_jira_ticket(file_name, old_hash, new_hash, severity, timestamp):

    try:
        auth = HTTPBasicAuth(EMAIL, API_TOKEN)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": f"FIM Alert: {file_name} modified",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"""File Integrity Monitoring Alert

File: {file_name}
Severity: {severity}
Old Hash: {old_hash}
New Hash: {new_hash}
Timestamp: {timestamp}"""
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Task"}
            }
        })

        response = requests.post(
            f"{JIRA_URL}/rest/api/3/issue",
            headers=headers,
            data=payload,
            auth=auth,
            timeout=10
        )

        if response.status_code != 201:
            print("Jira ticket creation failed:", response.text)
            return

        issue_key = response.json()["key"]
        print("Jira Ticket Created:", issue_key)

        # Upload log file
        try:
            attach_headers = {"X-Atlassian-Token": "no-check"}

            with open(LOG_FILE, "rb") as f:

                files = {"file": (LOG_FILE, f, "text/plain")}

                attach_response = requests.post(
                    f"{JIRA_URL}/rest/api/3/issue/{issue_key}/attachments",
                    headers=attach_headers,
                    files=files,
                    auth=auth
                )

            if attach_response.status_code in [200, 201]:
                print("Log file uploaded to Jira")

        except Exception as e:
            print("Log upload failed:", e)

    except Exception as e:
        print("Jira API error:", e)


# ---------- Log Writer ----------
def write_log(file_name, old_hash, new_hash, severity, timestamp):

    try:
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

    except Exception as e:
        print("Log writing failed:", e)


# ------- File hash calculation -----
def process_file(file_path, new_hashes):

    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        file_name = os.path.basename(file_path)
        current_time = time.ctime()

        new_hashes[file_name] = {
            "hash": file_hash,
            "timestamp": current_time
        }

    except Exception as e:
        print("Error processing file:", file_path, e)


# --------- Severity check -------
def get_priority(file_name):

    try:
        if 'passwd' in file_name or 'shadow' in file_name:
            return "critical"
        elif file_name.endswith(".exe") or file_name.endswith(".sh"):
            return "high"
        elif file_name.endswith(".log"):
            return "medium"
        else:
            return "low"

    except:
        return "low"


# -------- Create baseline --------
if not os.path.exists("baseline.json"):

    try:
        initial_hashes = {}

        for file in os.listdir(folder_path):

            full_path = os.path.join(folder_path, file)

            if os.path.isfile(full_path):
                process_file(full_path, initial_hashes)

        with open("baseline.json", "w") as f:
            json.dump(initial_hashes, f, indent=4)

        print("Baseline created")

    except Exception as e:
        print("Baseline creation failed:", e)


# -------- Monitoring Loop --------
while True:

    try:

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
                        create_jira_ticket(file, old_hash, new_hash, severity, timestamp)


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


    except Exception as e:
        print("Monitoring error:", e)

    time.sleep(10)