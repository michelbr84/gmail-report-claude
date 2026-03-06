---
name: gmail-attachments
description: >
  Attachment analysis skill. Reports on attachment-heavy traffic, large-file
  patterns, file type distribution, and periods with high file volume.
---

# gmail-attachments — Attachment Analysis

## Purpose

Analyze attachment patterns to understand file traffic volume, identify
large-file senders, and detect periods with unusually high attachment activity.

## Trigger

- `/gmail attachments month`
- Any command with `--has-attachments` flag

## What It Reports

- Total attachment count
- Total attachment size (MB/GB)
- Top file types (PDF, DOCX, images, etc.)
- Top senders by attachment volume
- Largest individual attachments
- Attachment trends over time

## Workflow

1. Fetch data for the period
2. Filter to messages with attachments
3. Extract attachment metadata (name, type, size)
4. Aggregate by sender, type, and period

## Output

- `GMAIL-REPORT-ATTACHMENTS.md`
