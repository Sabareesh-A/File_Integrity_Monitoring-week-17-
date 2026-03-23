# File Integrity Monitoring (FIM) Script Documentation

## Overview
This Python script monitors a specified folder for file changes, including modifications, deletions, and additions. When a change is detected, it logs the event, sends an email alert, and optionally creates a Jira ticket for high-severity changes.  

The script uses SHA-256 hashing to ensure file integrity and prioritizes alerts based on file type and sensitivity.

---

## Features
- Monitors file modifications, deletions, and additions.
- Generates SHA-256 hashes for file verification.
- Logs all events to `fim_log.log`.
- Sends email alerts for high and critical severity events.
- Creates Jira tickets for high and critical events.
- Maintains a baseline (`baseline.json`) to track file integrity.
- Stores priority alerts in `priority.json`.

---

## Prerequisites
- Python 3.8+
- Required libraries:
```bash
pip install python-dotenv requests
```
- Gmail account with app password for sending emails.
- Jira account and API token (for Jira ticket creation).

---

## Environment Variables
Create a `.env` file in the project root with the following variables:

```dotenv
EMAIL_SENDER=youremail@gmail.com
EMAIL_RECEIVER=receiveremail@gmail.com
EMAIL_PASSWORD=your_app_password
JIRA_URL=https://yourdomain.atlassian.net
JIRA_EMAIL=yourjiraemail@example.com
JIRA_TOKEN=your_jira_api_token
PROJECT_KEY=PROJECTKEY
```

---

## Configuration
- **Folder to monitor**: Set `folder_path` in the script.
- **Log file**: Defaults to `fim_log.log`.
- **Baseline file**: Defaults to `baseline.json`.
- **Priority file**: Defaults to `priority.json`.

---

## Severity Levels
The script assigns severity based on file type:
- `critical`: `passwd`, `shadow` files
- `high`: `.exe`, `.sh` files
- `medium`: `.log` files
- `low`: All other files

---

## Functions

### `send_email_alert(file_name, old_hash, new_hash, severity, timestamp)`
Sends an email with file change details.

### `create_jira_ticket(file_name, old_hash, new_hash, severity, timestamp)`
Creates a Jira ticket with file change details and uploads `fim_log.log`.

### `write_log(file_name, old_hash, new_hash, severity, timestamp)`
Appends file change information to `fim_log.log`.

### `process_file(file_path, new_hashes)`
Calculates SHA-256 hash for the file and updates `new_hashes`.

### `get_priority(file_name)`
Determines the severity level of a file.

---

## Usage
1. Place the script in your project folder.
2. Configure the `.env` file.
3. Ensure the folder to monitor exists and has test files.
4. Run the script:
```bash
python fim_monitor.py
```
5. The script continuously monitors the folder every 10 seconds.

---

## Example Log Entry
```
Fri Mar 24 14:23:45 2026
File: secret.txt
Severity: high
Old Hash: abc123...
New Hash: def456...
----------------------------------
```

---

## Notes
- Ensure that the Gmail account allows SMTP access via app passwords.
- Jira tickets are only created for `high` and `critical` severity files.
- Modify `folder_path` and severity rules as needed for your project requirements.

