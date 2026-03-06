#!/usr/bin/env python3
"""
fetch_gmail_data.py — Gmail API Data Retrieval and Normalization

Authenticates with Gmail API via OAuth, fetches messages for a given period,
and outputs normalized JSON for downstream analysis.

Usage:
    python3 fetch_gmail_data.py --period today --output data.json
    python3 fetch_gmail_data.py --from 2026-01-01 --to 2026-01-31 --output data.json
    python3 fetch_gmail_data.py --period month --include-spam --output data.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as dateparser

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Error: Gmail API dependencies not installed.")
    print("Run: pip install google-api-python-client google-auth google-auth-oauthlib")
    sys.exit(1)

# Gmail API scopes (read-only)
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def authenticate():
    """Authenticate with Gmail API via OAuth."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"Error: {CREDENTIALS_FILE} not found.")
                print("Download OAuth credentials from Google Cloud Console:")
                print("  https://console.cloud.google.com/apis/credentials")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def resolve_period(period=None, date_from=None, date_to=None):
    """Resolve period keyword or date range to start/end datetime."""
    now = datetime.now()

    if date_from and date_to:
        start = dateparser.parse(date_from)
        end = dateparser.parse(date_to)
    elif period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "week":
        start = now - timedelta(days=7)
        end = now
    elif period == "month":
        start = now - timedelta(days=30)
        end = now
    elif period == "year":
        start = now - timedelta(days=365)
        end = now
    else:
        print(f"Error: Unknown period '{period}'")
        sys.exit(1)

    return start, end


def fetch_messages(service, start, end, include_spam=False, max_results=500):
    """Fetch messages from Gmail for the given date range."""
    query = f"after:{start.strftime('%Y/%m/%d')} before:{end.strftime('%Y/%m/%d')}"

    label_ids = ["INBOX"]
    if include_spam:
        label_ids.append("SPAM")

    messages = []
    page_token = None

    while True:
        results = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=min(max_results - len(messages), 100),
                pageToken=page_token,
            )
            .execute()
        )

        batch = results.get("messages", [])
        if not batch:
            break

        for msg_ref in batch:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg_ref["id"], format="metadata")
                .execute()
            )
            messages.append(normalize_message(msg))

            if len(messages) >= max_results:
                break

        page_token = results.get("nextPageToken")
        if not page_token or len(messages) >= max_results:
            break

    return messages


def normalize_message(msg):
    """Normalize a Gmail API message into a flat dict."""
    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}

    return {
        "id": msg["id"],
        "thread_id": msg["threadId"],
        "date": headers.get("date", ""),
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "labels": msg.get("labelIds", []),
        "snippet": msg.get("snippet", ""),
        "size_estimate": msg.get("sizeEstimate", 0),
        "has_attachments": bool(msg.get("payload", {}).get("parts")),
        "is_unread": "UNREAD" in msg.get("labelIds", []),
        "is_spam": "SPAM" in msg.get("labelIds", []),
        "internal_date": msg.get("internalDate", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch Gmail data for reporting")
    parser.add_argument("--period", choices=["today", "week", "month", "year"])
    parser.add_argument("--from", dest="date_from", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", help="End date (YYYY-MM-DD)")
    parser.add_argument("--include-spam", action="store_true", help="Include spam messages")
    parser.add_argument("--max-results", type=int, default=500, help="Max messages to fetch")
    parser.add_argument("--output", default="gmail_data.json", help="Output file path")

    args = parser.parse_args()

    if not args.period and not (args.date_from and args.date_to):
        parser.error("Specify --period or both --from and --to")

    print(f"Authenticating with Gmail API...")
    service = authenticate()

    start, end = resolve_period(args.period, args.date_from, args.date_to)
    print(f"Fetching messages from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}...")

    messages = fetch_messages(service, start, end, args.include_spam, args.max_results)
    print(f"Fetched {len(messages)} messages.")

    output = {
        "period": {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "label": args.period or "custom",
        },
        "include_spam": args.include_spam,
        "total_messages": len(messages),
        "messages": messages,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    print(f"Data saved to {args.output}")


if __name__ == "__main__":
    main()
