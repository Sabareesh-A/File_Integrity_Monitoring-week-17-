import smtplib
from email.mime.text import MIMEText

def send_email():
    sender = "sabareeshanil02@gmail.com"
    receiver = "sabareesha.dev@gmail.com"
    app_password = "wtknbqrgohotfrus"

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
# Call function
send_email()