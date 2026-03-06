#!/usr/bin/env python3
"""
sender_ranker.py — Sender Aggregation and Ranking

Analyzes messages to rank senders by volume, classify them,
and calculate concentration metrics.

Usage:
    python3 sender_ranker.py data.json --top 20 --output senders.json
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict


def extract_email(from_header):
    """Extract email address from From header."""
    match = re.search(r'<([^>]+)>', from_header)
    if match:
        return match.group(1).lower()
    # Might be just an email without angle brackets
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', from_header)
    if match:
        return match.group(0).lower()
    return from_header.lower().strip()


def extract_domain(email):
    """Extract domain from email address."""
    parts = email.split("@")
    return parts[1] if len(parts) == 2 else email


def classify_sender(email, count, messages):
    """Classify sender as human, automated, newsletter, or notification."""
    domain = extract_domain(email)

    # Common automated/notification domains
    automated_patterns = [
        "noreply", "no-reply", "donotreply", "notifications",
        "alerts", "mailer-daemon", "postmaster"
    ]
    newsletter_patterns = [
        "newsletter", "news@", "digest", "weekly", "updates@",
        "marketing", "promo"
    ]

    email_lower = email.lower()

    for pattern in automated_patterns:
        if pattern in email_lower:
            return "automated"

    for pattern in newsletter_patterns:
        if pattern in email_lower:
            return "newsletter"

    # High-volume senders are likely automated
    if count > 50:
        return "likely-automated"

    return "human"


def main():
    parser = argparse.ArgumentParser(description="Rank Gmail senders")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("--top", type=int, default=20, help="Number of top senders")
    parser.add_argument("--output", default="senders.json", help="Output file")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])
    sender_counts = Counter()
    sender_messages = defaultdict(list)

    for msg in messages:
        email = extract_email(msg.get("from", ""))
        sender_counts[email] += 1
        sender_messages[email].append(msg)

    total = len(messages)
    unique_senders = len(sender_counts)

    # Build ranked list
    ranked = []
    for rank, (email, count) in enumerate(sender_counts.most_common(args.top), 1):
        ranked.append({
            "rank": rank,
            "email": email,
            "domain": extract_domain(email),
            "count": count,
            "percentage": round(count / total * 100, 1) if total > 0 else 0,
            "type": classify_sender(email, count, sender_messages[email]),
            "unread_count": sum(1 for m in sender_messages[email] if m.get("is_unread")),
        })

    # Concentration metrics
    top5_volume = sum(c for _, c in sender_counts.most_common(5))
    top10_volume = sum(c for _, c in sender_counts.most_common(10))

    result = {
        "total_messages": total,
        "unique_senders": unique_senders,
        "concentration": {
            "top5_count": top5_volume,
            "top5_percentage": round(top5_volume / total * 100, 1) if total > 0 else 0,
            "top10_count": top10_volume,
            "top10_percentage": round(top10_volume / total * 100, 1) if total > 0 else 0,
        },
        "top_senders": ranked,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Sender analysis: {unique_senders} unique senders, top 5 = {result['concentration']['top5_percentage']}%")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
