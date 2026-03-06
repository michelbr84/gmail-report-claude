#!/usr/bin/env python3
"""
generate_pdf_report.py — Professional PDF Report Generator

Creates a branded PDF report with cover page, charts, tables,
score breakdowns, and recommendations from Gmail analysis data.

Usage:
    python3 generate_pdf_report.py data.json GMAIL-REPORT.pdf
"""

import argparse
import json
import sys
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image
    )
except ImportError:
    print("Error: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not installed. Charts will be skipped.")


def create_cover_page(story, styles, data):
    """Create the report cover page."""
    story.append(Spacer(1, 2 * inch))

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        fontSize=28,
        spaceAfter=20,
        textColor=colors.HexColor("#1a73e8"),
    )
    story.append(Paragraph("Gmail Inbox Report", title_style))

    period = data.get("period", {})
    period_label = period.get("label", "custom").title()
    start = period.get("start", "")[:10]
    end = period.get("end", "")[:10]

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#5f6368"),
    )
    story.append(Paragraph(f"Period: {period_label} ({start} → {end})", subtitle_style))
    story.append(Spacer(1, 0.5 * inch))

    date_style = ParagraphStyle(
        "CoverDate",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.HexColor("#80868b"),
    )
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", date_style))

    filters = data.get("filters_applied", [])
    if filters:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(f"Filters: {', '.join(filters)}", date_style))

    story.append(PageBreak())


def create_summary_section(story, styles, data):
    """Create executive summary section."""
    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(Spacer(1, 0.2 * inch))

    total = data.get("total_messages", 0)
    period = data.get("period", {})
    label = period.get("label", "custom")

    summary_text = (
        f"This report analyzes <b>{total}</b> emails for the "
        f"<b>{label}</b> period. "
    )
    story.append(Paragraph(summary_text, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Key metrics table
    metrics = [
        ["Metric", "Value"],
        ["Total Messages", str(total)],
        ["Period", label.title()],
    ]

    messages = data.get("messages", [])
    unread = sum(1 for m in messages if m.get("is_unread"))
    spam = sum(1 for m in messages if m.get("is_spam"))

    metrics.append(["Unread Messages", str(unread)])
    metrics.append(["Spam Messages", str(spam)])
    metrics.append(["Read Rate", f"{round((total - unread) / total * 100, 1)}%" if total > 0 else "N/A"])

    table = Table(metrics, colWidths=[3 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a73e8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dadce0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5 * inch))


def create_volume_chart(messages, output_path):
    """Create a volume-over-time bar chart."""
    if not HAS_MATPLOTLIB:
        return None

    from collections import Counter
    from dateutil import parser as dateparser

    daily = Counter()
    for msg in messages:
        try:
            dt = dateparser.parse(msg.get("date", ""))
            if dt:
                daily[dt.strftime("%m/%d")] += 1
        except (ValueError, TypeError):
            continue

    if not daily:
        return None

    sorted_days = sorted(daily.items())
    dates = [d[0] for d in sorted_days]
    counts = [d[1] for d in sorted_days]

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.bar(dates, counts, color="#1a73e8", alpha=0.8)
    ax.set_ylabel("Messages")
    ax.set_title("Daily Email Volume")

    # Rotate labels if too many
    if len(dates) > 10:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate Gmail PDF report")
    parser.add_argument("input", help="Input Gmail data JSON file")
    parser.add_argument("output", nargs="?", default="GMAIL-REPORT.pdf", help="Output PDF path")

    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        args.output,
        pagesize=A4,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    # Cover page
    create_cover_page(story, styles, data)

    # Executive summary
    create_summary_section(story, styles, data)

    # Volume chart
    messages = data.get("messages", [])
    chart_path = create_volume_chart(messages, "/tmp/gmail_volume_chart.png")
    if chart_path:
        story.append(Paragraph("Daily Volume", styles["Heading2"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Image(chart_path, width=6 * inch, height=2.5 * inch))
        story.append(Spacer(1, 0.3 * inch))

    # Methodology
    story.append(PageBreak())
    story.append(Paragraph("Methodology", styles["Heading1"]))
    story.append(Spacer(1, 0.2 * inch))
    methodology_text = (
        "Gmail Inbox Score is calculated using a weighted methodology: "
        "Inbox Health & Workload (25%), Unread Backlog (20%), "
        "Spam/Noise Ratio (15%), Response Behavior (15%), "
        "Sender Concentration (10%), Label & Category Organization (10%), "
        "Attachment/File Load (5%). "
        "The score ranges from 0 to 100 and is designed to make "
        "reports comparable across time periods."
    )
    story.append(Paragraph(methodology_text, styles["Normal"]))

    # Build PDF
    doc.build(story)
    print(f"PDF report generated: {args.output}")


if __name__ == "__main__":
    main()
