# File Integrity Monitoring (FIM) Script Documentation

## Overview
This Python script implements a **File Integrity Monitoring (FIM)** system. It continuously monitors a specified directory for file changes such as:
- File modification
- File deletion
- New file creation

When changes are detected, the script:
- Logs the event
- Assigns a severity level
- Sends email alerts for high-risk changes

---

## Features
- SHA-256 hashing for file integrity verification
- Real-time monitoring using a loop
- Severity-based classification (Critical, High, Medium, Low)
- Email alerts for critical and high severity events
- Log file generation
- JSON-based baseline tracking

---

## Configuration

### Folder Path
```python
folder_path = "/Users/sabareeshanil/Desktop/fim/alert fim email/file-dir"
```
Directory to monitor.

### Log File
```python
LOG_FILE = "fim_log.log"
```
Stores all detected changes.

### Environment Variables (Required for Email Alerts)
Set the following variables:
- EMAIL_SENDER
- EMAIL_RECEIVER
- EMAIL_PASSWORD

---

## Modules Used
- `os` → File and directory handling
- `hashlib` → SHA-256 hashing
- `time` → Timestamp generation
- `json` → Baseline and priority storage
- `smtplib` → Email sending
- `email.mime.text` → Email formatting

---

## Function Breakdown

### 1. send_email_alert()
Sends an email when critical or high severity changes occur.

**Parameters:**
- file_name
- old_hash
- new_hash
- severity
- timestamp

**Functionality:**
- Creates email body
- Connects to SMTP server (Gmail)
- Sends alert

---

### 2. write_log()
Writes detected changes to a log file.

**Parameters:**
- file_name
- old_hash
- new_hash
- severity
- timestamp

---

### 3. process_file()
Calculates SHA-256 hash of a file.

**Parameters:**
- file_path
- new_hashes (dictionary)

**Output:**
Stores file hash and timestamp.

---

### 4. get_priority()
Assigns severity level based on file name/type.

**Rules:**
- Critical → contains "passwd" or "shadow"
- High → .exe, .sh files
- Medium → .log files
- Low → all others

---

## Workflow

### Step 1: Baseline Creation
- Runs only if `baseline.json` does not exist
- Stores initial file hashes

### Step 2: Monitoring Loop
Runs continuously every 10 seconds:

#### a. Scan Directory
- Generate new hashes

#### b. Compare with Baseline

**Modified Files:**
- Hash mismatch detected
- Logged and alerted (if high/critical)

**Deleted Files:**
- Present in baseline but missing now

**Added Files:**
- New files not in baseline

#### c. Update Files
- `priority.json` → stores categorized alerts
- `baseline.json` → updated with new hashes

---

## Output Files

### 1. baseline.json
Stores previous file states

### 2. priority.json
Stores categorized alerts:
```json
{
  "critical": [],
  "high": [],
  "medium": [],
  "low": []
}
```

### 3. fim_log.log
Human-readable log of all events

---

## Alert Behavior
- Email sent only for:
  - Critical
  - High

- Console message:
```
⚠️ Critical or High Priority Changes Detected
```

---

## Execution Flow
1. Create baseline (first run)
2. Start infinite loop
3. Scan directory
4. Compare hashes
5. Log changes
6. Send alerts if needed
7. Sleep for 10 seconds

---

## Security Notes
- Uses SHA-256 for strong hashing
- Email credentials should be stored securely (use app passwords for Gmail)
- Avoid hardcoding sensitive data

---

## Possible Improvements
- Add GUI dashboard
- Real-time notifications (Telegram/Slack)
- Recursive directory monitoring
- File size & metadata tracking
- Encryption for stored hashes

---

## Conclusion
This script provides a basic yet effective file integrity monitoring system suitable for detecting unauthorized changes in a directory. It can be extended for enterprise-level security monitoring solutions.

