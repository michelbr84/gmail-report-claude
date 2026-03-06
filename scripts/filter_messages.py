#!/usr/bin/env python3
"""
filter_messages.py — Message Filtering Engine

Applies filters to a Gmail data JSON file: date range, spam, unread,
labels, categories, senders, and attachments.

Usage:
    python3 filter_messages.py data.json --unread-only --exclude-spam
    python3 filter_messages.py data.json --label "Work" --sender user@example.com
    python3 filter_messages.py data.json --has-attachments --output filtered.json
"""

import argparse
import json
import sys


def load_data(filepath):
    """Load Gmail data from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_filters(messages, args):
    """Apply all specified filters to messages list."""
    filtered = messages

    # Spam filters
    if args.exclude_spam:
        filtered = [m for m in filtered if not m.get("is_spam", False)]
    elif not args.include_spam:
        filtered = [m for m in filtered if not m.get("is_spam", False)]

    # Read/unread filters
    if args.unread_only:
        filtered = [m for m in filtered if m.get("is_unread", False)]
    elif args.read_only:
        filtered = [m for m in filtered if not m.get("is_unread", False)]

    # Label filter
    if args.label:
        label_upper = args.label.upper()
        filtered = [
            m for m in filtered
            if any(label_upper in lbl.upper() for lbl in m.get("labels", []))
        ]

    # Category filter
    if args.category:
        cat_label = f"CATEGORY_{args.category.upper()}"
        filtered = [
            m for m in filtered
            if cat_label in m.get("labels", [])
        ]

    # Sender filter
    if args.sender:
        sender_lower = args.sender.lower()
        filtered = [
            m for m in filtered
            if sender_lower in m.get("from", "").lower()
        ]

    # Attachment filter
    if args.has_attachments:
        filtered = [m for m in filtered if m.get("has_attachments", False)]

    return filtered


def main():
    parser = argparse.ArgumentParser(description="Filter Gmail messages")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("--include-spam", action="store_true")
    parser.add_argument("--exclude-spam", action="store_true")
    parser.add_argument("--unread-only", action="store_true")
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--all-received", action="store_true")
    parser.add_argument("--label", help="Filter by Gmail label name")
    parser.add_argument("--category", help="Filter by category (primary, promotions, social, updates, forums)")
    parser.add_argument("--sender", help="Filter by sender email")
    parser.add_argument("--has-attachments", action="store_true")
    parser.add_argument("--output", help="Output file (default: overwrite input)")

    args = parser.parse_args()

    data = load_data(args.input)
    messages = data.get("messages", [])

    print(f"Loaded {len(messages)} messages from {args.input}")

    filtered = apply_filters(messages, args)

    print(f"After filtering: {len(filtered)} messages")

    # Build filter summary
    filters_applied = []
    if args.exclude_spam:
        filters_applied.append("exclude-spam")
    if args.include_spam:
        filters_applied.append("include-spam")
    if args.unread_only:
        filters_applied.append("unread-only")
    if args.read_only:
        filters_applied.append("read-only")
    if args.label:
        filters_applied.append(f"label:{args.label}")
    if args.category:
        filters_applied.append(f"category:{args.category}")
    if args.sender:
        filters_applied.append(f"sender:{args.sender}")
    if args.has_attachments:
        filters_applied.append("has-attachments")

    data["messages"] = filtered
    data["total_messages"] = len(filtered)
    data["filters_applied"] = filters_applied

    output_path = args.output or args.input
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    print(f"Filtered data saved to {output_path}")


if __name__ == "__main__":
    main()
