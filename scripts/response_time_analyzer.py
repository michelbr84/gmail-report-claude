#!/usr/bin/env python3
"""
response_time_analyzer.py — Reply Latency Estimation

Matches sent messages to received messages in the same thread
to estimate response times and follow-up behavior.

Usage:
    python3 response_time_analyzer.py data.json --output response.json
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser as dateparser


def parse_date(date_str):
    """Parse date string from message data."""
    try:
        return dateparser.parse(date_str)
    except (ValueError, TypeError):
        return None


def analyze_threads(messages):
    """Group messages by thread and identify reply pairs."""
    threads = defaultdict(list)

    for msg in messages:
        threads[msg.get("thread_id", "")].append(msg)

    reply_pairs = []

    for thread_id, thread_msgs in threads.items():
        # Sort by date
        sorted_msgs = sorted(
            thread_msgs,
            key=lambda m: parse_date(m.get("date", "")) or datetime.min,
        )

        for i in range(1, len(sorted_msgs)):
            prev = sorted_msgs[i - 1]
            curr = sorted_msgs[i]

            prev_dt = parse_date(prev.get("date", ""))
            curr_dt = parse_date(curr.get("date", ""))

            if not prev_dt or not curr_dt:
                continue

            # Check if current is a sent message (reply to received)
            is_sent = "SENT" in curr.get("labels", [])
            is_prev_received = "SENT" not in prev.get("labels", [])

            if is_sent and is_prev_received:
                latency = curr_dt - prev_dt
                reply_pairs.append({
                    "thread_id": thread_id,
                    "received_date": prev_dt.isoformat(),
                    "replied_date": curr_dt.isoformat(),
                    "latency_seconds": int(latency.total_seconds()),
                    "latency_human": format_duration(latency),
                    "subject": prev.get("subject", ""),
                    "from": prev.get("from", ""),
                })

    return reply_pairs


def format_duration(delta):
    """Format a timedelta into human-readable string."""
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        return f"{total_seconds // 60}m"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        return f"{days}d {hours}h"


def find_needing_followup(messages, max_wait_hours=48):
    """Find threads where a received message has no reply after max_wait_hours."""
    threads = defaultdict(list)

    for msg in messages:
        threads[msg.get("thread_id", "")].append(msg)

    needs_followup = []
    cutoff = datetime.now() - timedelta(hours=max_wait_hours)

    for thread_id, thread_msgs in threads.items():
        sorted_msgs = sorted(
            thread_msgs,
            key=lambda m: parse_date(m.get("date", "")) or datetime.min,
        )

        if not sorted_msgs:
            continue

        last = sorted_msgs[-1]
        last_dt = parse_date(last.get("date", ""))

        if not last_dt:
            continue

        # If last message is received (not sent) and older than cutoff
        is_received = "SENT" not in last.get("labels", [])
        if is_received and last_dt < cutoff:
            waiting_hours = (datetime.now() - last_dt).total_seconds() / 3600
            needs_followup.append({
                "thread_id": thread_id,
                "subject": last.get("subject", ""),
                "from": last.get("from", ""),
                "last_received": last_dt.isoformat(),
                "waiting_hours": round(waiting_hours, 1),
            })

    return sorted(needs_followup, key=lambda x: x["waiting_hours"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Analyze Gmail response times")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("--followup-hours", type=int, default=48, help="Hours before flagging as needing follow-up")
    parser.add_argument("--output", default="response.json", help="Output file")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])

    reply_pairs = analyze_threads(messages)
    needs_followup = find_needing_followup(messages, args.followup_hours)

    # Statistics
    if reply_pairs:
        latencies = [p["latency_seconds"] for p in reply_pairs]
        avg_latency = sum(latencies) / len(latencies)
        sorted_latencies = sorted(latencies)
        median_latency = sorted_latencies[len(sorted_latencies) // 2]
        min_latency = min(latencies)
        max_latency = max(latencies)
    else:
        avg_latency = median_latency = min_latency = max_latency = 0

    result = {
        "total_replies": len(reply_pairs),
        "threads_needing_followup": len(needs_followup),
        "statistics": {
            "average_seconds": round(avg_latency),
            "average_human": format_duration(timedelta(seconds=avg_latency)),
            "median_seconds": median_latency,
            "median_human": format_duration(timedelta(seconds=median_latency)),
            "fastest_seconds": min_latency,
            "fastest_human": format_duration(timedelta(seconds=min_latency)),
            "slowest_seconds": max_latency,
            "slowest_human": format_duration(timedelta(seconds=max_latency)),
        },
        "reply_pairs": reply_pairs[:50],  # Limit to top 50
        "needs_followup": needs_followup[:20],  # Limit to top 20
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Replies: {len(reply_pairs)} | Avg: {result['statistics']['average_human']} | Median: {result['statistics']['median_human']}")
    print(f"Threads needing follow-up: {len(needs_followup)}")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
