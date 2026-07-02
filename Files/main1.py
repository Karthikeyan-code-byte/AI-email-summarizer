# ==========================================================
# AI EMAIL ASSISTANT - VERSION 2.0 STABLE
# PART 1
# Imports + Configuration + Login + Menus
# ==========================================================

import os
import base64
import re
import json
import ollama

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# ==========================================================
# CONFIGURATION
# ==========================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

CLIENT_SECRET = "client_secret_402880942204-u5836fofnqrvuht7l8qfn0vtrf37ooh3.apps.googleusercontent.com.json"

TOKEN_DIR = "tokens"
REPORT_DIR = "reports"
LOG_DIR = "logs"

MAX_EMAILS = 20

MODEL_NAME = "qwen2.5:3b"


# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

for folder in [TOKEN_DIR, REPORT_DIR, LOG_DIR]:

    if not os.path.exists(folder):
        os.makedirs(folder)


# ==========================================================
# GET AVAILABLE ACCOUNTS
# ==========================================================

def get_accounts():

    accounts = []

    for file in os.listdir(TOKEN_DIR):

        if file.endswith(".json"):
            accounts.append(file[:-5])

    return sorted(accounts)


# ==========================================================
# ACCOUNT MENU
# ==========================================================

def choose_account():

    accounts = get_accounts()

    print("\n" + "=" * 60)
    print("🤖 AI EMAIL ASSISTANT")
    print("=" * 60)

    if len(accounts) == 0:

        print("\nNo Gmail accounts found.")
        print("Let's add your first Gmail account.\n")

        account_name = input("Enter account name : ").strip()

        return account_name

    print("\nAvailable Gmail Accounts\n")

    for index, account in enumerate(accounts, start=1):

        print(f"{index}. {account}")

    print(f"{len(accounts)+1}. Add New Gmail Account")

    while True:

        try:

            choice = int(input("\nChoose an option : "))

            if 1 <= choice <= len(accounts):

                return accounts[choice-1]

            elif choice == len(accounts)+1:

                account = input(
                    "\nEnter new account name : "
                ).strip()

                return account

            else:

                print("Invalid choice.")

        except ValueError:

            print("Enter a valid number.")


# ==========================================================
# TIME RANGE MENU
# ==========================================================

def choose_time_range():

    print("\n" + "=" * 60)
    print("📅 EMAIL TIME RANGE")
    print("=" * 60)

    print("1. Today's Emails")
    print("2. Last 7 Days")
    print("3. Last 30 Days")
    print("4. All Emails")

    while True:

        choice = input("\nChoose : ")

        if choice == "1":

            return "newer_than:1d"

        elif choice == "2":

            return "newer_than:7d"

        elif choice == "3":

            return "newer_than:30d"

        elif choice == "4":

            return ""

        else:

            print("Invalid option.")


# ==========================================================
# GMAIL LOGIN
# ==========================================================

def gmail_login(account_name):

    token_path = os.path.join(
        TOKEN_DIR,
        account_name + ".json"
    )

    creds = None

    if os.path.exists(token_path):

        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:

            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


# ==========================================================
# PROGRAM START
# ==========================================================

account_name = choose_account()

gmail_service = gmail_login(account_name)

time_filter = choose_time_range()

print("\n")
print("=" * 60)
print("Logged in as :", account_name)
print("Time Filter  :", time_filter if time_filter else "All Emails")
print("=" * 60)

# ==========================================================
# PART 2
# GMAIL READER + EMAIL BODY EXTRACTION
# ==========================================================

from html import unescape


# ==========================================================
# EXTRACT EMAIL BODY
# ==========================================================

def get_email_body(payload):

    """
    Extracts plain text or HTML email body.
    """

    body = ""

    # ------------------------------------------------------

    if "parts" in payload:

        for part in payload["parts"]:

            mime = part.get("mimeType", "")

            # Plain text
            if mime == "text/plain":

                data = part["body"].get("data")

                if data:

                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

            # HTML Email
            elif mime == "text/html":

                data = part["body"].get("data")

                if data:

                    html = base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

                    html = unescape(html)

                    html = re.sub(
                        "<[^<]+?>",
                        " ",
                        html
                    )

                    body = html

    else:

        data = payload["body"].get("data")

        if data:

            body = base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

    return body.strip()


# ==========================================================
# READ EMAILS
# ==========================================================

def get_emails(service, query):

    print("\nFetching emails...\n")

    results = service.users().messages().list(

        userId="me",

        q=query,

        maxResults=MAX_EMAILS

    ).execute()

    messages = results.get("messages", [])

    if len(messages) == 0:

        print("\nNo emails found.")

        return []

    emails = []

    print(f"Found {len(messages)} email(s).\n")

    for index, message in enumerate(messages, start=1):

        print(f"Reading email {index}/{len(messages)}...")

        msg = service.users().messages().get(

            userId="me",

            id=message["id"],

            format="full"

        ).execute()

        headers = msg["payload"]["headers"]

        sender = "Unknown"

        subject = "No Subject"

        date = ""

        for header in headers:

            if header["name"] == "From":

                sender = header["value"]

            elif header["name"] == "Subject":

                subject = header["value"]

            elif header["name"] == "Date":

                date = header["value"]

        body = get_email_body(
            msg["payload"]
        )

        if body == "":

            body = msg.get(
                "snippet",
                ""
            )

        email = {

            "sender": sender,

            "subject": subject,

            "date": date,

            "body": body,

            "snippet": msg.get(
                "snippet",
                ""
            )

        }

        emails.append(email)

    return emails


# ==========================================================
# LOAD EMAILS
# ==========================================================

emails = get_emails(

    gmail_service,

    time_filter

)

print("\n")
print("=" * 60)
print(f"Emails Loaded : {len(emails)}")
print("=" * 60)

# ----------------------------------------------------------
# TEST OUTPUT
# ----------------------------------------------------------

for email in emails:

    print("\n" + "=" * 60)

    print("Sender :")
    print(email["sender"])

    print("\nSubject :")
    print(email["subject"])

    print("\nDate :")
    print(email["date"])

    print("\nSnippet :")
    print(email["snippet"])

    print("\nBody Preview :")

    print(email["body"][:300])

print("\n")
print("=" * 60)
print("Finished Reading Emails")
print("=" * 60)

# ==========================================================
# PART 3
# AI EMAIL ANALYZER
# ==========================================================

def summarize_email(email):

    prompt = f"""
You are an intelligent AI Email Assistant.

Analyze the email carefully.

Return ONLY in the following format.

Summary:
(2-3 concise lines)

Deadline:
(Write None if no deadline exists.)

Action Required:
(Write None if no action is required.)

Priority:
High / Medium / Low

Category:
Choose ONE only.

Internship
Placement
Hackathon
College
Research
Meeting
Banking
Shopping
Social
Promotion
Personal
Other

Priority Rules

HIGH
- Deadlines
- Interviews
- Placements
- Internships
- Hackathons
- Banking Alerts
- Security Alerts

MEDIUM
- Meetings
- College Circulars
- Research Updates
- Notifications

LOW
- Shopping
- Promotions
- Advertisements
- Social Emails

EMAIL

Sender:
{email["sender"]}

Subject:
{email["subject"]}

Body:
{email["body"][:2500]}
"""

    response = ollama.chat(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response["message"]["content"]


# ==========================================================
# AI ANALYSIS
# ==========================================================

print("\n")
print("=" * 70)
print("🤖 GENERATING AI SUMMARIES")
print("=" * 70)

high = 0
medium = 0
low = 0

report = []

for index, email in enumerate(emails, start=1):

    print(f"\nAnalyzing Email {index}/{len(emails)}...")

    ai_summary = summarize_email(email)

    report.append({

        "sender": email["sender"],

        "subject": email["subject"],

        "date": email["date"],

        "summary": ai_summary

    })

    text = ai_summary.lower()

    if "priority: high" in text or "priority:\nhigh" in text:

        high += 1

    elif "priority: medium" in text or "priority:\nmedium" in text:

        medium += 1

    else:

        low += 1

print("\n")
print("=" * 70)
print("AI ANALYSIS COMPLETE")
print("=" * 70)

# ==========================================================
# SAVE REPORT
# ==========================================================

from datetime import datetime

filename = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S.txt"
)

filepath = os.path.join(
    REPORT_DIR,
    filename
)

with open(filepath, "w", encoding="utf-8") as file:

    file.write("AI EMAIL REPORT\n")
    file.write("=" * 60 + "\n\n")

    for email in report:

        file.write(
            f"Sender : {email['sender']}\n"
        )

        file.write(
            f"Subject : {email['subject']}\n\n"
        )

        file.write(email["summary"])

        file.write("\n")

        file.write("=" * 60)

        file.write("\n\n")

print("\n")
print("📁 Report Saved")

print(filepath)

