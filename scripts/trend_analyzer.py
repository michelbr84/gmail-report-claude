#!/usr/bin/env python3
"""
trend_analyzer.py — Time-Series Analysis

Analyzes email volume trends over time, detecting spikes,
seasonality, and directional changes.

Usage:
    python3 trend_analyzer.py data.json --granularity day --output trends.json
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from dateutil import parser as dateparser


def parse_date(date_str):
    """Parse date string from message data."""
    try:
        return dateparser.parse(date_str)
    except (ValueError, TypeError):
        return None


def aggregate_by_granularity(messages, granularity):
    """Group messages by time granularity."""
    buckets = Counter()

    for msg in messages:
        dt = parse_date(msg.get("date", ""))
        if not dt:
            continue

        if granularity == "hour":
            key = dt.strftime("%Y-%m-%d %H:00")
        elif granularity == "day":
            key = dt.strftime("%Y-%m-%d")
        elif granularity == "week":
            key = dt.strftime("%Y-W%W")
        elif granularity == "month":
            key = dt.strftime("%Y-%m")
        else:
            key = dt.strftime("%Y-%m-%d")

        buckets[key] += 1

    return dict(sorted(buckets.items()))


def detect_spikes(timeline, threshold=2.0):
    """Detect spikes above threshold standard deviations."""
    if not timeline:
        return []

    values = list(timeline.values())
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std_dev = variance ** 0.5

    if std_dev == 0:
        return []

    spikes = []
    for period, count in timeline.items():
        z_score = (count - mean) / std_dev
        if z_score > threshold:
            spikes.append({
                "period": period,
                "count": count,
                "z_score": round(z_score, 2),
                "above_average_by": round(count - mean, 1),
            })

    return spikes


def calculate_trend(timeline):
    """Calculate trend direction using simple linear regression."""
    if len(timeline) < 2:
        return "insufficient_data"

    values = list(timeline.values())
    n = len(values)
    x_mean = (n - 1) / 2
    y_mean = sum(values) / n

    numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return "stable"

    slope = numerator / denominator

    # Classify trend
    relative_slope = slope / y_mean if y_mean > 0 else 0

    if relative_slope > 0.05:
        return "increasing"
    elif relative_slope < -0.05:
        return "decreasing"
    else:
        return "stable"


def main():
    parser = argparse.ArgumentParser(description="Analyze email trends")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("--granularity", default="day", choices=["hour", "day", "week", "month"])
    parser.add_argument("--output", default="trends.json", help="Output file")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])
    timeline = aggregate_by_granularity(messages, args.granularity)

    values = list(timeline.values())
    total = sum(values)
    avg = round(total / len(values), 1) if values else 0
    peak_period = max(timeline, key=timeline.get) if timeline else None
    quietest_period = min(timeline, key=timeline.get) if timeline else None

    result = {
        "granularity": args.granularity,
        "periods": len(timeline),
        "total_messages": total,
        "average_per_period": avg,
        "peak_period": peak_period,
        "peak_count": timeline.get(peak_period, 0) if peak_period else 0,
        "quietest_period": quietest_period,
        "quietest_count": timeline.get(quietest_period, 0) if quietest_period else 0,
        "trend": calculate_trend(timeline),
        "spikes": detect_spikes(timeline),
        "timeline": timeline,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Trend: {result['trend']} | Avg: {avg}/{args.granularity} | Peak: {peak_period} ({result['peak_count']})")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
