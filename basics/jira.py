import requests
import json
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://sabareeshadev.atlassian.net"
EMAIL = "sabareesha.dev@gmail.com"
API_TOKEN = "ATATT3xFfGF0C2dlZ-lYhd5tf4XOj-Bm0p3pvc6ToKkM-OJ4ATo8NnkaUXZRFobNPbHa2nQvW7BNtQo8Y0thgYhla6HCP2gVVVxPQcSreKoR6ZHTxMUuhkur74FXIYDkh0FK7eEPyZ4lfpeVdTzpncOqQvyhPXVA3VsmxTkVd1rFM3vRQQiph5M=9F81CEDA"
PROJECT_KEY = "PDM"

auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = json.dumps({
    "fields": {
        "project": {
            "key": PROJECT_KEY
        },
        "summary": "FIM Python Test Ticket",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "This ticket was created using Python Jira API."
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Task"
        }
    }
})

response = requests.post(
    f"{JIRA_URL}/rest/api/3/issue",
    headers=headers,
    data=payload,
    auth=auth
)

print("Status Code:", response.status_code)
print("Response:", response.text)
