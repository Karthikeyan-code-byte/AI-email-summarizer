# AI-email-summarizer

# 🤖 AI Email Assistant

An AI-powered Gmail automation tool built with **Python**, **Gmail API**, and **Ollama (Qwen 2.5)** that automatically reads emails, generates intelligent summaries, identifies deadlines, detects priorities, categorizes emails, and creates daily reports.

This project runs **completely on your local machine**, ensuring your email content remains private.

---

## ✨ Features

- 📧 Read emails securely using the Gmail API
- 🔐 OAuth 2.0 authentication with multi-account support
- 👤 Switch between multiple Gmail accounts
- 📅 Select email time range
  - Today's Emails
  - Last 7 Days
  - Last 30 Days
  - All Emails
- 🤖 AI-powered email summarization using Ollama
- ⭐ Automatic priority detection
  - High
  - Medium
  - Low
- 📂 Automatic email categorization
- 📅 Deadline extraction
- ✅ Action required detection
- 📄 Automatic report generation
- 💻 Fully local AI processing (no cloud AI required)

---

## 🛠 Technologies Used

- Python 3.11+
- Gmail API
- Google OAuth 2.0
- Ollama
- Qwen 2.5 (Local LLM)
- Google API Python Client

---

## 📂 Project Structure

```
EmailSummariser/
│
├── main.py
├── client_secret.json
├── requirements.txt
│
├── tokens/
│   ├── personal.json
│   ├── college.json
│
├── reports/
│
└── logs/
```

---

## ⚙ Installation

### 1. Clone the repository

install the python file (main1) and requirements file from the files folder

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Ollama

Download Ollama from

https://ollama.com

---

### 4. Download the AI Model

```bash
ollama pull qwen2.5:3b
```

---

### 5. Configure Gmail API

1. Create a project in Google Cloud Console.
2. Enable Gmail API.
3. Create OAuth Desktop Credentials.
4. Download the JSON credentials.
5. Rename it as:

```
client_secret.json
```

6. Place it inside the project folder.

---

## ▶ Running the Project

```bash
python main1.py
```

---

## 📋 Application Workflow

```
Start Program
      │
      ▼
Select Gmail Account
      │
      ▼
Choose Email Time Range
      │
      ▼
Authenticate Gmail
      │
      ▼
Read Emails
      │
      ▼
Extract Email Body
      │
      ▼
Generate AI Summary
      │
      ▼
Detect Priority
      │
      ▼
Detect Category
      │
      ▼
Extract Deadline
      │
      ▼
Generate Report
```

---

## 📊 AI Output

Each email includes

- Sender
- Subject
- Date
- AI Summary
- Deadline
- Action Required
- Priority
- Category

---

## 🔒 Privacy

This project processes emails locally using Ollama.

No email content is sent to cloud AI services.

---

## 🚀 Future Improvements

- PDF report generation
- Excel report export
- Google Calendar integration
- Smart spam filtering
- AI email search
- Email dashboard
- Telegram/WhatsApp notifications
- Outlook support
- Voice assistant integration

---

## 📸 Example Output

```
=====================================================

📧 Sender
Google

📌 Subject
Security Alert

🤖 AI Summary

Summary:
New sign-in detected.

Deadline:
None

Action Required:
Review account activity.

Priority:
High

Category:
Security

=====================================================
```

---

## 🤝 Contributions

Contributions, suggestions, and feature requests are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author
Developed by Karthikeyan D
