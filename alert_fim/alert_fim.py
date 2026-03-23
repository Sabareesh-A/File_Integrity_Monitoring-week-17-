import os
import hashlib
import time
import json
import smtplib
from email.mime.text import MIMEText


folder_path = "/Users/sabareeshanil/Desktop/fim/alert_fim/file-dir"



#-------file hash calculation-----
def process_file(file_path, new_hashes):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    file_name = os.path.basename(file_path)
    current_time = time.ctime()

    new_hashes[file_name] = {
        "hash": file_hash,
        "timestamp": current_time
    }
#------------------------------


#---------severity check-------
def get_priority(file_name):
    if 'passwd' in file_name or 'shadow' in file_name:
        return "critical"
    elif file_name.endswith(".exe") or file_name.endswith(".sh"):
        return "high"
    elif file_name.endswith(".log"):
        return "medium"
    else:
        return "low"
#-----------------------------


#-------email alert function------
def send_email():
    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    app_password = os.getenv("EMAIL_PASSWORD")

    subject = "Test Email"
    body = "A critical or high priority change has been detected in the monitored directory.\nPlease review the changes immediately."

    # Create message
    msg = MIMEText(body)
    msg["Subject"] = "Alert: Critical or High Priority Changes Detected"
    msg["From"] = "FIM Alert System"
    msg["To"] = "SOC Team"

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, app_password)

        # Send email
        server.sendmail(sender, receiver, msg.as_string())
        print("Email sent successfully!")

        server.quit()

    except Exception as e:
        print("Error:", e)

#-----------------------------------    



if not os.path.exists("baseline.json"):
    initial_hashes = {}
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            process_file(full_path, initial_hashes)

    with open("baseline.json", "w") as f:
        json.dump(initial_hashes, f, indent=4)

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

    for file in existing_hashes:
        if file in new_hashes:
            if existing_hashes[file]["hash"] != new_hashes[file]["hash"]:
                severity = get_priority(file)
                priority[severity].append(file + " modified at " + new_hashes[file]["timestamp"])

    for file in existing_hashes:
        if file not in new_hashes:
            severity = get_priority(file)
            priority[severity].append(file + " deleted at " + time.ctime())

    for file in new_hashes:
        if file not in existing_hashes:
            severity = get_priority(file)
            priority[severity].append(file + " added at " + new_hashes[file]["timestamp"])

    with open("priority.json", "w") as f:
        json.dump(priority, f, indent=4)

    with open("baseline.json", "w") as f:
        json.dump(new_hashes, f, indent=4)

    if priority["critical"] or priority["high"]:
        print("Critical or High Priority Changes Detected⚠️:")
        send_email()




    time.sleep(10)
